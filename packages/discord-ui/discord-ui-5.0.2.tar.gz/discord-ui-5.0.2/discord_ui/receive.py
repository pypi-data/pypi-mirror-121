from .slash.http import ModifiedSlashState
from .errors import InvalidEvent, OutOfValidRange, WrongType
from .slash.errors import AlreadyDeferred, EphemeralDeletion
from .tools import MISSING, setup_logger, _none, get, _default
from .slash.types import ContextCommand, SlashCommand, SlashOption, SlashPermission, SlashSubcommand
from .http import BetterRoute, jsonifyMessage, send_files
from .components import ActionRow, Button, LinkButton, SelectMenu, SelectOption, UseableComponent, make_component

import discord
from discord.ext.commands import Bot
from discord.errors import HTTPException
from discord.state import ConnectionState

from typing import Any, List, Union, Dict
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

logging = setup_logger("discord-ui")


class InteractionType:
    PING                                =       Ping        =           1
    APPLICATION_COMMAND                 =      Command      =           2
    MESSAGE_COMPONENT                   =     Component     =           3
    APPLICATION_COMMAND_AUTOCOMPLETE    =    Autocomplete   =           4

class Interaction():
    def __init__(self, state, data, user=None, message=None) -> None:
        self._state: ModifiedSlashState = state

        self.deferred: bool = False
        self.responded: bool = False
        self._deferred_hidden: bool = False
        self._original_payload: dict = data

        self.author: Union[discord.Member, discord.User] = user
        """The user who created the interaction"""
        self.application_id: int = data["application_id"]
        """The ID of the bot application"""
        self.token: str = data["token"]
        """The token for responding to the interaction"""
        self.id: int = data["id"]
        """The id of the interaction"""
        self.type: int = data["type"]
        """The type of the interaction. See :class:`~InteractionType` for more information"""
        self.version: int = data["version"]
        self.data: dict = data["data"]
        """The passed data of the interaction"""
        self.channel_id: int = int(data.get("channel_id")) if data.get("channel_id") is not None else None
        """The channel-id where the interaction was created"""
        self.guild_id: int = int(data["guild_id"]) if data.get("guild_id") is not None else None
        """The guild-id where the interaction was created"""
        self.message: Message = message
        """The message of the interaction"""

    @property
    def guild(self) -> discord.Guild:
        """
        The guild where the interaction was created
        
        :type: :class:`discord.Guild`
        """
        return self._state._get_guild(self.guild_id)
    @property
    def channel(self) -> Union[discord.TextChannel, discord.DMChannel]:
        """
        The channel where the interaction was created
        
        :type: :class:`discord.TextChannel` | :class:`discord.DMChannel`
        """
        return self._state.get_channel(self.channel_id) or self._state.get_channel(self.author.id)

    async def defer(self, hidden=False):
        """
        This will acknowledge the interaction. This will show the (*Bot* is thinking...) Dialog

        .. note::
            
            This function should be used if the bot needs more than 15 seconds to respond
        
        Parameters
        ----------
            hidden: :class:`bool`, optional
                Whether the loading thing should be only visible to the user; default False.
        
        """
        if self.deferred:
            logging.error(AlreadyDeferred())
            return

        payload = None
        if hidden is True:
            payload = {"flags": 64}
            self._deferred_hidden = True
        
        await self._state.slash_http.respond_to(self.id, self.token, 5, payload)
        self.deferred = True

    async def respond(self, content=MISSING, *, tts=False, embed=MISSING, embeds=MISSING, file=MISSING, files=MISSING, nonce=MISSING,
    allowed_mentions=MISSING, mention_author=MISSING, components=MISSING, delete_after=MISSING, listener=MISSING, 
    hidden=False, ninja_mode=False) -> Union['Message', 'EphemeralMessage']:
        """
        Responds to the interaction
        
        Parameters
        ----------
        content: :class:`str`, optional
            The raw message content
        tts: :class:`bool`
            Whether the message should be send with text-to-speech
        embed: :class:`discord.Embed`
            Embed rich content
        embeds: List[:class:`discord.Embed`]
            A list of embeds for the message
        file: :class:`discord.File`
            The file which will be attached to the message
        files: List[:class:`discord.File`]
            A list of files which will be attached to the message
        nonce: :class:`int`
            The nonce to use for sending this message
        allowed_mentions: :class:`discord.AllowedMentions`
            Controls the mentions being processed in this message
        mention_author: :class:`bool`
            Whether the author should be mentioned
        components: List[:class:`~Button` | :class:`~LinkButton` | :class:`~SelectMenu`]
            A list of message components to be included
        delete_after: :class:`float`
            After how many seconds the message should be deleted, only works for non-hiddend messages; default MISSING
        listener: :class:`Listener`
            A component-listener for this message
        hidden: :class:`bool`
            Whether the response should be visible only to the user 
        ninja_mode: :class:`bool`
            If true, the client will respond to the button interaction with almost nothing and returns nothing
        
        Returns
        -------
        :return: Returns the sent message
        :type: :class:`~Message` | :class:`EphemeralMessage`
        """
        if ninja_mode is True or all(y in [MISSING, False] for x, y in locals().items() if x not in ["self"]):
            try:
                await self._state.slash_http.respond_to(self.id, self.token, 6)
                return
            except HTTPException as x:
                if "value must be one of (4, 5)" in str(x).lower():
                    logging.warning(str(x) + "\n" + "The 'ninja_mode' parameter is not supported for slash commands!")
                    ninja_mode = False
                else:
                    raise x

        if self.responded is True:
            return await self.send(content=content, tts=tts, embed=embed, embeds=embeds, nonce=nonce, allowed_mentions=allowed_mentions, mention_author=mention_author, components=components, listener=listener, hidden=hidden)

        if components is MISSING and listener is not MISSING:
            components = listener.to_components()        
        payload = jsonifyMessage(content=content, tts=tts, embed=embed, embeds=embeds, nonce=nonce, allowed_mentions=allowed_mentions, mention_author=mention_author, components=components)
        
        if self._deferred_hidden is hidden:
            if self._deferred_hidden is False and hidden is True:
                logging.warning("Your response should be hidden, but the interaction was deferred public. This results in a public response.")
            if self._deferred_hidden is True and hidden is False:
                logging.warning("Your response should be public, but the interaction was deferred hidden. This results in a hidden response.")
        hide_message = self._deferred_hidden or not self.deferred and hidden is True


        r = None
        if delete_after is not MISSING and hide_message is True:
            raise EphemeralDeletion()

        if hide_message:
            payload["flags"] = 64
        
        if self.deferred:
            route = BetterRoute("PATCH", f'/webhooks/{self.application_id}/{self.token}/messages/@original')
            if file is not MISSING or files is not MISSING:
                await send_files(route=route, files=[file] if files is MISSING else files, payload=payload, http=self._state.http)
            else:
                await self._state.http.request(route, json=payload)    
        else:
            await self._state.slash_http.respond_to(self.id, self.token, 4, payload, files=[file] if file is not MISSING else _default(None, files))
        self.responded = True
        
        r = await self._state.http.request(BetterRoute("GET", f"/webhooks/{self.application_id}/{self.token}/messages/@original"))
        if hide_message is True:
            msg = EphemeralMessage(state=self._state, channel=self.channel, data=r, application_id=self.application_id, token=self.token)
        else:
            msg = await getMessage(self._state, data=r, response=False)
        if listener is not MISSING:
            listener._start(msg)
        if not _none(delete_after):
            await msg.delete(delete_after)
        return msg
    async def send(self, content=None, *, tts=False, embed=MISSING, embeds=MISSING, file=MISSING, files=MISSING, nonce=MISSING,
    allowed_mentions=MISSING, mention_author=MISSING, components=MISSING, delete_after=MISSING, listener=MISSING, hidden=False) -> Union['Message', 'EphemeralMessage']:
        """
        Sends a message to the interaction using a webhook
        
        Parameters
        ----------
        content: :class:`str`, optional
            The raw message content
        tts: :class:`bool` 
            Whether the message should be send with text-to-speech
        embed: :class:`discord.Embed`
            Embed rich content
        embeds: List[:class:`discord.Embed`]
            A list of embeds for the message
        file: :class:`discord.File`
            The file which will be attached to the message
        files: List[:class:`discord.File`]
            A list of files which will be attached to the message
        nonce: :class:`int`
            The nonce to use for sending this message
        allowed_mentions: :class:`discord.AllowedMentions`
            Controls the mentions being processed in this message
        mention_author: :class:`bool`
            Whether the author should be mentioned
        components: List[:class:`~Button` | :class:`~LinkButton` | :class:`~SelectMenu`]
            A list of message components to be included
        delete_after: :class:`float`
            After how many seconds the message should be deleted, only works for non-hiddend messages; default MISSING
        listener: :class:`Listener`
            A component-listener for this message
        hidden: :class:`bool`
            Whether the response should be visible only to the user 
        ninja_mode: :class:`bool`
            If true, the client will respond to the button interaction with almost nothing and returns nothing
        
        Returns
        -------
        :return: Returns the sent message
        :type: :class:`~Message` | :class:`EphemeralMessage`
        """
        if self.responded is False:
            return await self.respond(content=content, tts=tts, embed=embed, embeds=embeds, file=file, files=files, nonce=nonce, allowed_mentions=allowed_mentions, mention_author=mention_author, components=components, delete_after=delete_after, listener=listener, hidden=hidden)

        if components is MISSING and listener is not MISSING:
            components = listener.to_components()
        payload = jsonifyMessage(content=content, tts=tts, embed=embed, embeds=embeds, nonce=nonce, allowed_mentions=allowed_mentions, mention_author=mention_author, components=components)
        
        if hidden:
            payload["flags"] = 64

        route = BetterRoute("POST", f'/webhooks/{self.application_id}/{self.token}')
        if file is not MISSING or files is not MISSING:
            r = await send_files(route=route, files=[file] if files is MISSING else files, payload=payload, http=self._state.http)
        else:
            r = await self._state.http.request(route, json=payload)

        if hidden is True:
            msg = EphemeralMessage(state=self._state, channel=self._state.get_channel(int(r["channel_id"])), data=r, application_id=self.application_id, token=self.token)
        else:
            msg = await getMessage(self._state, r, response=False)
        if delete_after is not MISSING:
            await msg.delete(delete_after)
        if listener is not MISSING:
            listener._start(msg)
        return msg
    def _handle_auto_defer(self, auto_defer):
        self.deferred = auto_defer[0]
        self._deferred_hidden = auto_defer[1]

class ChoiceGeneratorContext(Interaction):
    """A class for information that could be needed for generating choices for autocomopletion"""
    def __init__(self, command, state, data, options, user=None) -> None:
        Interaction.__init__(self, state, data, user=user)
        self.focused_option: dict = options[get(options, check=lambda x: options[x].get("focused", False))]
        """The option for which the choices should be generated"""
        self.value_query: Union[str, int] = self.focused_option["value"]
        """The current 'query' for the value"""
        self.selected_options: Dict[str, Any] = {options[x]["name"]: options[x]["value"] for x in options}
        """All the options that were already selected"""
        self.command: Union[SlashedCommand, SlashedCommand, SlashedContext] = command
        """The slash command for which the choices should be generated"""

    async def defer(self, *args, **kwargs):
        """Cannot defer this type of interaction"""
        raise NotImplementedError()
    async def respond(self, *args, **kwargs):
        """Cannot rerspond to this type of interaction"""
        raise NotImplementedError()
    async def send(self, *args, **kwargs):
        """Cannot send followup message to this type of interaction"""
        raise NotImplementedError()

class ComponentContext(Interaction, UseableComponent):
    """A received component"""
    def __init__(self, state, data, user, message) -> None:
        Interaction.__init__(self, state, data, user=user, message=message)
        UseableComponent.__init__(self, data["data"]["component_type"])

class SelectedMenu(Interaction, SelectMenu):
    """A :class:`~SelectMenu` object in which an item was selected"""
    def __init__(self, data, user, s, msg, client) -> None:
        Interaction.__init__(self, client._connection, data, user, msg)
        default = [i for i, o in enumerate(s.options) if o.default is True]
        SelectMenu.__init__(self, s.custom_id, s.options, s.min_values, s.max_values, s.placeholder, default[0] if len(default) == 1 else None, s.disabled)
        
        self.bot: Bot = client
        self.selected_options: List[SelectOption] = []
        """The list of the selected options"""
        self.selected_values: List[str] = []
        """The list of raw values which were selected"""
        for val in data["data"]["values"]:
            for x in self.options:
                if x.value == val:
                    self.selected_options.append(x)
                    self.selected_values.append(x.value)
        self.author: discord.Member = user
        """The user who selected the value"""

class PressedButton(Interaction, Button):
    """A :class:`~Button` object that was pressed"""
    def __init__(self, data, user, b, message, client) -> None:
        Interaction.__init__(self, client._connection, data, user, message)
        Button.__init__(self, b.custom_id, b.label, b.color, b.emoji, b.new_line, b.disabled)

        self._json = b.to_dict()
        self.bot: Bot = client
        self.author: discord.Member = user
        """The user who pressed the button"""

class SlashedCommand(Interaction, SlashCommand):
    """A :class:`~SlashCommand` object that was used"""
    def __init__(self, client, command: SlashCommand, data, user, args = None) -> None:
        Interaction.__init__(self, client._connection, data, user)
        SlashCommand.__init__(self, command.callback, command.name, command.description, command.options, guild_ids=command.guild_ids, guild_permissions=command.guild_permissions)
        for x in self.__slots__:
            setattr(self, x, getattr(command, x))

        self.bot: Bot = client
        self._json = command.to_dict()
        self.author: discord.Member = user
        """The user who used the command"""
        self.args: Dict[str, Union[str, int, bool, discord.Member, discord.TextChannel, discord.Role, float]] = args
        """The options that were received"""
        self.permissions: SlashPermission = command.guild_permissions.get(self.guild_id) if command.guild_permissions is not None else None
        """The permissions for this guild"""
class SlashedSubCommand(SlashedCommand, SlashSubcommand):
    """A Sub-:class:`~SlashCommand` command that was used"""
    def __init__(self, client, command, data, user, args = None) -> None:
        SlashedCommand.__init__(self, client, command, data, user, args)
        SlashSubcommand.__init__(self, command.callback, command.base_names, command.name, command.description, command.options, command.guild_ids, command.default_permission, command.guild_permissions)
            

class SlashedContext(Interaction, ContextCommand):
    def __init__(self, client, command: ContextCommand, data, user, param) -> None:
        Interaction.__init__(self, client._connection, data, user)
        ContextCommand.__init__(self, command.command_type, command.callback, command.name, guild_ids=command.guild_ids, guild_permissions=command.guild_permissions)
        for x in self.__slots__:
            setattr(self, x, getattr(command, x))
        
        self._json = command.to_dict()
        self.bot: Bot = client
        self.param: Union[Message, discord.Member, discord.User] = param
        """The parameter that was received"""
        self.permissions: SlashPermission = command.guild_permissions.get(self.guild_id) if command.guild_permissions is not None else None 
        """The permissions for this guild"""
        


async def getMessage(state: ConnectionState, data, response=True):
    """
    Async function to get the response message

    Parameters
    -----------------

    state: :class:`discord.state.ConnectionState`
        The discord bot client
    data: :class:`dict`
        The raw data
    user: :class:`discord.User`
        The User which pressed the button
    response: :class:`bool`
        Whether the Message returned should be of type `ResponseMessage` or `Message`
    channel: :class:`discord.Messageable`
        An alternative channel that will be used when no channel was found

    Returns
    -------
    :class:`~Message` | :class:`~EphemeralMessage`
        The sent message
    """
    msg_base = data.get("message", data)

    channel = state.get_channel(int(data["channel_id"])) or state.get_channel(int(msg_base["author"]["id"]))
    if response:
        if msg_base["flags"] == 64:
            return EphemeralResponseMessage(state=state, channel=channel, data=data.get("message", data))
        return Message(state=state, channel=channel, data=msg_base)

    if msg_base["flags"] == 64:
        return EphemeralMessage(state=state, channel=channel, data=msg_base)
    return Message(state=state, channel=channel, data=msg_base)

class Message(discord.Message):
    """A fixed :class:`discord.Message` optimized for components"""
    def __init__(self, *, state, channel, data):
        self.__slots__ = discord.Message.__slots__ + ("components", "supressed")
        self._payload = data

        self._state: ConnectionState = None
        discord.Message.__init__(self, state=state, channel=channel, data=data)
        self.components: List[Union[Button, LinkButton, SelectMenu]] = []
        """The components in the message
        
        :type: List[]:class:`~Button` | :class:`~LinkButton` | :class:`SelectMenu`]
        """
        self.suppressed = False
        self._update_components(data)

    # region attributes
    @property
    def buttons(self) -> List[Union[Button, LinkButton]]:
        """The button components in the message
        
        :type: List[:class:`~Button` | :class:`~LinkButton`]
        """
        if hasattr(self, "components") and self.components is not None:
            return [x for x in self.components if isinstance(x, (Button, LinkButton))]
        return []
    @property
    def select_menus(self) -> List[SelectMenu]:
        """The select menus components in the message

        :type: List[:class:`~SelectMenu`]
        """
        if hasattr(self, "components") and self.components is not None:
            return [x for x in self.components if isinstance(x, SelectMenu)]
        return []
    @property
    def action_row(self) -> ActionRow:
        return ActionRow(self.components)
    # endregion

    def _update_components(self, data):
        """Updates the message components"""
        if data.get("components") is None:
            self.components = []
            return
        self.components = []
        if len(data["components"]) == 0:
            pass
        elif len(data["components"]) > 1:
            # multiple lines
            for componentWrapper in data["components"]:
                # newline
                for index, com in enumerate(componentWrapper["components"]):
                    self.components.append(make_component(com, index==0))
        elif len(data["components"][0]["components"]) > 1:
            # All inline
            for index, com in enumerate(data["components"][0]["components"]):
                self.components.append(make_component(com, index==0))
        else:
            # One button
            component = data["components"][0]["components"][0]
            self.components.append(make_component(component))

    def _update(self, data):
        super()._update(data)
        self._update_components(data)

    async def edit(self, content=MISSING, *, embed=MISSING, embeds=MISSING, attachments=MISSING, suppress=MISSING, 
        delete_after=MISSING, allowed_mentions=MISSING, components=MISSING):
        """Edits the message and updates its properties

        .. note::

            If a paremeter is `None`, the attribute will be removed from the message

        Parameters
        ----------------
        content: :class:`str`
            The new message content
        embed: :class:`discord.Embed`
            The new embed of the message
        embeds: List[:class:`discord.Embed`]
            The new list of discord embeds
        attachments: List[:class:`discord.Attachment`]
            A list of new attachments
        supress: :class:`bool`
            Whether the embeds should be shown
        delete_after: :class:`float`
            After how many seconds the message should be deleted
        allowed_mentions: :class:`discord.AllowedMentions`
            The mentions proceeded in the message
        components: List[:class:`~Button` | :class:`~LinkButton` | :class:`~SelectMenu`]
            A list of components to be included the message
        """
        payload = jsonifyMessage(content, embed=embed, embeds=embeds, allowed_mentions=allowed_mentions, attachments=attachments, suppress=suppress, flags=self.flags.value, components=components)
        data = await self._state.http.edit_message(self.channel.id, self.id, **payload)
        self._update(data)

        if delete_after is not MISSING:
            await self.delete(delay=delete_after)

    async def disable_action_row(self, row, disable = True):
        """Disables an action row of components in the message
        
        Parameters
        ----------
            row: :class:`int` |  :class:`range`
                Which rows to disable, first row is ``0``; If row parameter is of type :class:`int`, the nth row will be disabled, if type is :class:`range`, the range is going to be iterated and all rows in the range will be disabled

            disable: :class:`bool`, optional
                Whether to disable (``True``) or enable (``False``) the components; default True

        Raises
        ------
            :raises: :class:`discord_ui.errors.OutOfValidRange` : The specified range was out of the possible range of the component rows 
            :raises: :class:`discord_ui.errors.OutOfValidRange` : The specified row was out of the possible range of the component rows
        
        """
        comps = []
        if isinstance(row, range):
            for i, _ in enumerate(self.action_rows):
                if i >= len(self.action_rows) - 1 or i < 0:
                    raise OutOfValidRange("row[" + str(i) + "]", 0, len(self.action_rows) - 1)
                for comp in self.action_rows[i]:
                    if i in row:
                        comp.disabled = disable
                    comps.append(comp)
        else:
            for i, _ in enumerate(self.action_rows):
                if i >= len(self.action_rows) - 1 or i < 0:
                    raise OutOfValidRange("row", 0, len(self.action_rows) - 1)
                for comp in self.action_rows[i]:
                    if i == row:
                        comp.disabled = disable
                    comps.append(comp)
        await self.edit(components=comps)

    async def disable_components(self, disable = True):
        """Disables all component in the message
        
        Parameters
        ----------
            disable: :class:`bool`, optional
                Whether to disable (``True``) or enable (``False``) als components; default True
        
        """
        fixed = []
        for x in self.components:
            x.disabled = disable
            fixed.append(x)
        await self.edit(components=fixed)

    @property
    def action_rows(self):
        """The action rows in the message

        :type: List[:class:`~Button` | :class:`LinkButton` | :class:`SelectMenu`]
        """
        rows: List[List[Union[Button, LinkButton, SelectMenu]]] = []

        c_row = []
        i = 0
        for x in self.components:
            if getattr(x, 'new_line', True) == True and i > 0:
                rows.append(ActionRow(c_row))
                c_row = []
            c_row.append(x)
            i += 1
        if len(c_row) > 0:
            rows.append(c_row) 
        return rows

    async def wait_for(self, event_name: Literal["select", "button", "component"], client, custom_id=None, by=None, check=lambda component: True, timeout=None) -> Union[PressedButton, SelectedMenu, ComponentContext]:
        """Waits for a message component to be invoked in this message

        Parameters
        -----------
            event_name: :class:`str`
                The name of the event which will be awaited [``"select"`` | ``"button"`` | ``"component"``]
                
                .. note::

                    ``event_name`` must be ``select`` for a select menu selection, ``button`` for a button press and ``component`` for any component

            client: :class:`discord.ext.commands.Bot`
                The discord client
            custom_id: :class:`str`, Optional
                Filters the waiting for a custom_id
            by: :class:`discord.User` | :class:`discord.Member` | :class:`int` | :class:`str`, Optional
                The user or the user id by that has to create the component interaction
            check: :class:`function`, Optional
                A check that has to return True in order to break from the event and return the received component
                    The function takes the received component as the parameter
            timeout: :class:`float`, Optional
                After how many seconds the waiting should be canceled. 
                Throws an :class:`asyncio.TimeoutError` Exception

        Raises
        ------
            :raises: :class:`discord_ui.errors.InvalidEvent` : The event name passed was invalid 

        Returns
        ----------
            :returns: The component that was waited for
            :type: :class:`~PressedButton` | :class:`~SelectedMenu`

        Example
        ---------

        .. code-block::

            # send a message with comoponents
            msg = await ctx.send("okayy", components=[Button("a_custom_id", ...)])
            try:
                # wait for the button
                btn = await msg.wait_for("button", client, "a_custom_id", by=ctx.author, timeout=20)
                # send response
                btn.respond()
            except asyncio.TimeoutError:
                # no button press was received in 20 seconds timespan
        """
        def _check(com):
            if com.message.id == self.id:
                statements = []
                if not _none(custom_id):
                    statements.append(com.custom_id == custom_id)
                if not _none(by):
                    statements.append(com.author.id == (by.id if hasattr(by, "id") else int(by)))
                if not _none(check):
                    statements.append(check(com))
                return all(statements)
            return False
        if not isinstance(client, Bot):
            raise WrongType("client", client, "discord.ext.commands.Bot")
        
        if event_name.lower() == "button":
            return await client.wait_for('button_press', check=_check, timeout=timeout)
        if event_name.lower() == "select":
            return await client.wait_for("menu_select", check=_check, timeout=timeout)
        if event_name.lower() == "component":
            return await client.wait_for("component", check=_check, timeout=timeout)
        
        raise InvalidEvent(event_name, ["button", "select", "component"])

    async def put_listener(self, listener):
        """Adds a listener to this message and edits it if the components are missing
        
        Parameters
        ----------
        listener: :class:`Listener`
            The listener which should be put to the message
        
        """
        if len(self.components) == 0:
            await self.edit(components=listener.to_components())
        self.attach_listener(listener)
        
    def attach_listener(self, listener):
        """Attaches a listener to this message after it was sent
        
        Parameters
        ----------
        listener: :class:`Listener`
            The listener that should be attached
        
        """
        listener._start(self)
    def remove_listener(self):
        """Removes the listener from this message"""
        try:
            del self._state._component_listeners[str(self.id)]
        except KeyError:
            pass


class WebhookMessage(Message, discord.WebhookMessage):
    def __init__(self, *, state, channel, data):
        Message.__init__(self, state=state, channel=channel, data=data)
        discord.WebhookMessage.__init__(self, state=state, channel=channel, data=data)
    async def edit(self, *args, **fields):
        """Edits the message

        content: :class:`str`, Optional
            The content to edit the message with or None to clear it.
        embed: :class:`discord.Embed`
            Embed rich content
        embeds: List[:class:`discord.Embed`], Optional
            A list of embeds to edit the message with.
        supress: :class:`bool`
            Whether to supress all embeds in the message
        allowed_mentions: :class`discord.AllowedMentions`
            Controls the mentions being processed in this message. See `discord.abc.Messageable.send` for more information.
        """
        return await self._state._webhook._adapter.edit_webhook_message(message_id=self.id, payload=jsonifyMessage(*args, **fields))
    

class EphemeralMessage(Message):
    """Represents a hidden (ephemeral) message"""
    def __init__(self, state, channel, data, application_id=None, token=None):
        #region fix reference keyerror
        if data.get("message_reference"):
            if data["message_reference"].get("channel_id") is None:
                data["message_reference"]["channel_id"] = str(channel.id)
        #endregion
        Message.__init__(self, state=state, channel=channel, data=data)
        self._application_id = application_id
        self._interaction_token = token
    async def edit(self, *args, **fields):
        r = BetterRoute("PATCH", f"/webhooks/{self._application_id}/{self._interaction_token}/messages/{self.id}")
        self._update(await self._state.http.request(r, json=jsonifyMessage(*args, **fields)))        
    async def delete(self):
        """Override for delete function that will throw an exception"""
        raise EphemeralDeletion()

class EphemeralResponseMessage(Message):
    """A ephemeral message wich was created from an interaction
    
    .. important::

        Methods like `.edit()`, which change the original message, need a `token` paremeter passed in order to work
    """
    def __init__(self, *, state, channel, data):
        Message.__init__(self, state=state, channel=channel, data=data)

    async def edit(self, token, *args, **fields):
        """Edits the message
        
        Parameters
        ----------
            token: :class:`str`
                The token of the interaction with wich this ephemeral message was sent
            fields: :class:`kwargs`
                The fields to edit (ex. `content="...", embed=..., attachments=[...]`)

            Example

            .. code-block::

                async def testing(ctx):
                    msg = await ctx.send("hello hidden world", components=[Button("test")])
                    btn = await msg.wait_for("button", client)
                    await btn.message.edit(ctx.token, content="edited", components=None)
        
        """
        route = BetterRoute("PATCH", f"/webhooks/{self.interaction.application_id}/{token}/messages/{self.id}")
        self._update(await self._state.http.request(route, json=jsonifyMessage(*args, **fields)))
    async def delete(self):
        """Override for delete function that will throw an exception"""
        raise EphemeralDeletion()
    async def disable_components(self, token, disable = True):
        """Disables all component in the message
        
        Parameters
        ----------
            disable: :class:`bool`, optional
                Whether to disable (``True``) or enable (``False``) als components; default True
        
        """
        fixed = []
        for x in self.components:
            x.disabled = disable
            fixed.append(x)
        await self.edit(token, components=fixed)
