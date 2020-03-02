from __future__ import annotations

from typing import *
from typing.io import *


class __Dynamic:

    def __new__(cls, *args, **kwargs):
        from tinybot.webapi import DynamicDictObject
        
        return DynamicDictObject({**{}, **kwargs})


class Update:
    """
    This object represents an incoming update.
    At most one of the optional parameters can be present in any given update.
    """

    def __init__(self, update_id: int, message: Optional[Message] = None, edited_message: Optional[Message] = None, channel_post: Optional[Message] = None, edited_channel_post: Optional[Message] = None, inline_query: Optional[InlineQuery] = None, chosen_inline_result: Optional[ChosenInlineResult] = None, callback_query: Optional[CallbackQuery] = None, shipping_query: Optional[ShippingQuery] = None, pre_checkout_query: Optional[PreCheckoutQuery] = None, poll: Optional[Poll] = None, poll_answer: Optional[PollAnswer] = None):
        """
        :param update_id: The update‘s unique identifier. Update identifiers start from a certain positive number and increase sequentially. This ID becomes especially handy if you’re using Webhooks, since it allows you to ignore repeated updates or to restore the correct update sequence, should they get out of order. If there are no new updates for at least a week, then identifier of the next update will be chosen randomly instead of sequentially.
        :param message: Optional. New incoming message of any kind — text, photo, sticker, etc.
        :param edited_message: Optional. New version of a message that is known to the bot and was edited
        :param channel_post: Optional. New incoming channel post of any kind — text, photo, sticker, etc.
        :param edited_channel_post: Optional. New version of a channel post that is known to the bot and was edited
        :param inline_query: Optional. New incoming inline query
        :param chosen_inline_result: Optional. The result of an inline query that was chosen by a user and sent to their chat partner. Please see our documentation on the feedback collecting for details on how to enable these updates for your bot.
        :param callback_query: Optional. New incoming callback query
        :param shipping_query: Optional. New incoming shipping query. Only for invoices with flexible price
        :param pre_checkout_query: Optional. New incoming pre-checkout query. Contains full information about checkout
        :param poll: Optional. New poll state. Bots receive only updates about stopped polls and polls, which are sent by the bot
        :param poll_answer: Optional. A user changed their answer in a non-anonymous poll. Bots receive new votes only in polls that were sent by the bot itself.
        """
        self.update_id = update_id
        self.message = message
        self.edited_message = edited_message
        self.channel_post = channel_post
        self.edited_channel_post = edited_channel_post
        self.inline_query = inline_query
        self.chosen_inline_result = chosen_inline_result
        self.callback_query = callback_query
        self.shipping_query = shipping_query
        self.pre_checkout_query = pre_checkout_query
        self.poll = poll
        self.poll_answer = poll_answer


class WebhookInfo:
    """Contains information about the current status of a webhook."""

    def __init__(self, url: str, has_custom_certificate: bool, pending_update_count: int, last_error_date: Optional[int] = None, last_error_message: Optional[str] = None, max_connections: Optional[int] = None, allowed_updates: Optional[List[str]] = None):
        """
        :param url: Webhook URL, may be empty if webhook is not set up
        :param has_custom_certificate: True, if a custom certificate was provided for webhook certificate checks
        :param pending_update_count: Number of updates awaiting delivery
        :param last_error_date: Optional. Unix time for the most recent error that happened when trying to deliver an update via webhook
        :param last_error_message: Optional. Error message in human-readable format for the most recent error that happened when trying to deliver an update via webhook
        :param max_connections: Optional. Maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery
        :param allowed_updates: Optional. A list of update types the bot is subscribed to. Defaults to all update types
        """
        self.url = url
        self.has_custom_certificate = has_custom_certificate
        self.pending_update_count = pending_update_count
        self.last_error_date = last_error_date
        self.last_error_message = last_error_message
        self.max_connections = max_connections
        self.allowed_updates = allowed_updates


class User:
    """This object represents a Telegram user or bot."""

    def __init__(self, id_: int, is_bot: bool, first_name: str, last_name: Optional[str] = None, username: Optional[str] = None, language_code: Optional[str] = None, can_join_groups: Optional[bool] = None, can_read_all_group_messages: Optional[bool] = None, supports_inline_queries: Optional[bool] = None):
        """
        :param id_: Unique identifier for this user or bot
        :param is_bot: True, if this user is a bot
        :param first_name: User‘s or bot’s first name
        :param last_name: Optional. User‘s or bot’s last name
        :param username: Optional. User‘s or bot’s username
        :param language_code: Optional. IETF language tag of the user's language
        :param can_join_groups: Optional. True, if the bot can be invited to groups. Returned only in getMe.
        :param can_read_all_group_messages: Optional. True, if privacy mode is disabled for the bot. Returned only in getMe.
        :param supports_inline_queries: Optional. True, if the bot supports inline queries. Returned only in getMe.
        """
        self.id_ = id_
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code
        self.can_join_groups = can_join_groups
        self.can_read_all_group_messages = can_read_all_group_messages
        self.supports_inline_queries = supports_inline_queries


class Chat:
    """This object represents a chat."""

    def __init__(self, id_: int, type_: str, title: Optional[str] = None, username: Optional[str] = None, first_name: Optional[str] = None, last_name: Optional[str] = None, photo: Optional[ChatPhoto] = None, description: Optional[str] = None, invite_link: Optional[str] = None, pinned_message: Optional[Message] = None, permissions: Optional[ChatPermissions] = None, slow_mode_delay: Optional[int] = None, sticker_set_name: Optional[str] = None, can_set_sticker_set: Optional[bool] = None):
        """
        :param id_: Unique identifier for this chat. This number may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier.
        :param type_: Type of chat, can be either “private”, “group”, “supergroup” or “channel”
        :param title: Optional. Title, for supergroups, channels and group chats
        :param username: Optional. Username, for private chats, supergroups and channels if available
        :param first_name: Optional. First name of the other party in a private chat
        :param last_name: Optional. Last name of the other party in a private chat
        :param photo: Optional. Chat photo. Returned only in getChat.
        :param description: Optional. Description, for groups, supergroups and channel chats. Returned only in getChat.
        :param invite_link: Optional. Chat invite link, for groups, supergroups and channel chats. Each administrator in a chat generates their own invite links, so the bot must first generate the link using exportChatInviteLink. Returned only in getChat.
        :param pinned_message: Optional. Pinned message, for groups, supergroups and channels. Returned only in getChat.
        :param permissions: Optional. Default chat member permissions, for groups and supergroups. Returned only in getChat.
        :param slow_mode_delay: Optional. For supergroups, the minimum allowed delay between consecutive messages sent by each unpriviledged user. Returned only in getChat.
        :param sticker_set_name: Optional. For supergroups, name of group sticker set. Returned only in getChat.
        :param can_set_sticker_set: Optional. True, if the bot can change the group sticker set. Returned only in getChat.
        """
        self.id_ = id_
        self.type_ = type_
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo
        self.description = description
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.permissions = permissions
        self.slow_mode_delay = slow_mode_delay
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set


class Message:
    """This object represents a message."""

    def __init__(self, message_id: int, date: int, chat: Chat, from_: Optional[User] = None, forward_from: Optional[User] = None, forward_from_chat: Optional[Chat] = None, forward_from_message_id: Optional[int] = None, forward_signature: Optional[str] = None, forward_sender_name: Optional[str] = None, forward_date: Optional[int] = None, reply_to_message: Optional[Message] = None, edit_date: Optional[int] = None, media_group_id: Optional[str] = None, author_signature: Optional[str] = None, text: Optional[str] = None, entities: Optional[List[MessageEntity]] = None, caption_entities: Optional[List[MessageEntity]] = None, audio: Optional[Audio] = None, document: Optional[Document] = None, animation: Optional[Animation] = None, game: Optional[Game] = None, photo: Optional[List[PhotoSize]] = None, sticker: Optional[Sticker] = None, video: Optional[Video] = None, voice: Optional[Voice] = None, video_note: Optional[VideoNote] = None, caption: Optional[str] = None, contact: Optional[Contact] = None, location: Optional[Location] = None, venue: Optional[Venue] = None, poll: Optional[Poll] = None, new_chat_members: Optional[List[User]] = None, left_chat_member: Optional[User] = None, new_chat_title: Optional[str] = None, new_chat_photo: Optional[List[PhotoSize]] = None, delete_chat_photo: Optional[bool] = None, group_chat_created: Optional[bool] = None, supergroup_chat_created: Optional[bool] = None, channel_chat_created: Optional[bool] = None, migrate_to_chat_id: Optional[int] = None, migrate_from_chat_id: Optional[int] = None, pinned_message: Optional[Message] = None, invoice: Optional[Invoice] = None, successful_payment: Optional[SuccessfulPayment] = None, connected_website: Optional[str] = None, passport_data: Optional[PassportData] = None, reply_markup: Optional[InlineKeyboardMarkup] = None):
        """
        :param message_id: Unique message identifier inside this chat
        :param from_: Optional. Sender, empty for messages sent to channels
        :param date: Date the message was sent in Unix time
        :param chat: Conversation the message belongs to
        :param forward_from: Optional. For forwarded messages, sender of the original message
        :param forward_from_chat: Optional. For messages forwarded from channels, information about the original channel
        :param forward_from_message_id: Optional. For messages forwarded from channels, identifier of the original message in the channel
        :param forward_signature: Optional. For messages forwarded from channels, signature of the post author if present
        :param forward_sender_name: Optional. Sender's name for messages forwarded from users who disallow adding a link to their account in forwarded messages
        :param forward_date: Optional. For forwarded messages, date the original message was sent in Unix time
        :param reply_to_message: Optional. For replies, the original message. Note that the Message object in this field will not contain further reply_to_message fields even if it itself is a reply.
        :param edit_date: Optional. Date the message was last edited in Unix time
        :param media_group_id: Optional. The unique identifier of a media message group this message belongs to
        :param author_signature: Optional. Signature of the post author for messages in channels
        :param text: Optional. For text messages, the actual UTF-8 text of the message, 0-4096 characters
        :param entities: Optional. For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text
        :param caption_entities: Optional. For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear in the caption
        :param audio: Optional. Message is an audio file, information about the file
        :param document: Optional. Message is a general file, information about the file
        :param animation: Optional. Message is an animation, information about the animation. For backward compatibility, when this field is set, the document field will also be set
        :param game: Optional. Message is a game, information about the game. More about games »
        :param photo: Optional. Message is a photo, available sizes of the photo
        :param sticker: Optional. Message is a sticker, information about the sticker
        :param video: Optional. Message is a video, information about the video
        :param voice: Optional. Message is a voice message, information about the file
        :param video_note: Optional. Message is a video note, information about the video message
        :param caption: Optional. Caption for the animation, audio, document, photo, video or voice, 0-1024 characters
        :param contact: Optional. Message is a shared contact, information about the contact
        :param location: Optional. Message is a shared location, information about the location
        :param venue: Optional. Message is a venue, information about the venue
        :param poll: Optional. Message is a native poll, information about the poll
        :param new_chat_members: Optional. New members that were added to the group or supergroup and information about them (the bot itself may be one of these members)
        :param left_chat_member: Optional. A member was removed from the group, information about them (this member may be the bot itself)
        :param new_chat_title: Optional. A chat title was changed to this value
        :param new_chat_photo: Optional. A chat photo was change to this value
        :param delete_chat_photo: Optional. Service message: the chat photo was deleted
        :param group_chat_created: Optional. Service message: the group has been created
        :param supergroup_chat_created: Optional. Service message: the supergroup has been created. This field can‘t be received in a message coming through updates, because bot can’t be a member of a supergroup when it is created. It can only be found in reply_to_message if someone replies to a very first message in a directly created supergroup.
        :param channel_chat_created: Optional. Service message: the channel has been created. This field can‘t be received in a message coming through updates, because bot can’t be a member of a channel when it is created. It can only be found in reply_to_message if someone replies to a very first message in a channel.
        :param migrate_to_chat_id: Optional. The group has been migrated to a supergroup with the specified identifier. This number may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier.
        :param migrate_from_chat_id: Optional. The supergroup has been migrated from a group with the specified identifier. This number may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier.
        :param pinned_message: Optional. Specified message was pinned. Note that the Message object in this field will not contain further reply_to_message fields even if it is itself a reply.
        :param invoice: Optional. Message is an invoice for a payment, information about the invoice. More about payments »
        :param successful_payment: Optional. Message is a service message about a successful payment, information about the payment. More about payments »
        :param connected_website: Optional. The domain name of the website on which the user has logged in. More about Telegram Login »
        :param passport_data: Optional. Telegram Passport data
        :param reply_markup: Optional. Inline keyboard attached to the message. login_url buttons are represented as ordinary url buttons.
        """
        self.message_id = message_id
        self.from_ = from_
        self.date = date
        self.chat = chat
        self.forward_from = forward_from
        self.forward_from_chat = forward_from_chat
        self.forward_from_message_id = forward_from_message_id
        self.forward_signature = forward_signature
        self.forward_sender_name = forward_sender_name
        self.forward_date = forward_date
        self.reply_to_message = reply_to_message
        self.edit_date = edit_date
        self.media_group_id = media_group_id
        self.author_signature = author_signature
        self.text = text
        self.entities = entities
        self.caption_entities = caption_entities
        self.audio = audio
        self.document = document
        self.animation = animation
        self.game = game
        self.photo = photo
        self.sticker = sticker
        self.video = video
        self.voice = voice
        self.video_note = video_note
        self.caption = caption
        self.contact = contact
        self.location = location
        self.venue = venue
        self.poll = poll
        self.new_chat_members = new_chat_members
        self.left_chat_member = left_chat_member
        self.new_chat_title = new_chat_title
        self.new_chat_photo = new_chat_photo
        self.delete_chat_photo = delete_chat_photo
        self.group_chat_created = group_chat_created
        self.supergroup_chat_created = supergroup_chat_created
        self.channel_chat_created = channel_chat_created
        self.migrate_to_chat_id = migrate_to_chat_id
        self.migrate_from_chat_id = migrate_from_chat_id
        self.pinned_message = pinned_message
        self.invoice = invoice
        self.successful_payment = successful_payment
        self.connected_website = connected_website
        self.passport_data = passport_data
        self.reply_markup = reply_markup


class MessageEntity:
    """This object represents one special entity in a text message. For example, hashtags, usernames, URLs, etc."""

    def __init__(self, type_: str, offset: int, length: int, url: Optional[str] = None, user: Optional[User] = None, language: Optional[str] = None):
        """
        :param type_: Type of the entity. Can be “mention” (@username), “hashtag” (#hashtag), “cashtag” ($USD), “bot_command” (/start@jobs_bot), “url” (https://telegram.org), “email” (do-not-reply@telegram.org), “phone_number” (+1-212-555-0123), “bold” (bold text), “italic” (italic text), “underline” (underlined text), “strikethrough” (strikethrough text), “code” (monowidth string), “pre” (monowidth block), “text_link” (for clickable text URLs), “text_mention” (for users without usernames)
        :param offset: Offset in UTF-16 code units to the start of the entity
        :param length: Length of the entity in UTF-16 code units
        :param url: Optional. For “text_link” only, url that will be opened after user taps on the text
        :param user: Optional. For “text_mention” only, the mentioned user
        :param language: Optional. For “pre” only, the programming language of the entity text
        """
        self.type_ = type_
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
        self.language = language


class PhotoSize:
    """This object represents one size of a photo or a file / sticker thumbnail."""

    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int, file_size: Optional[int] = None):
        """
        :param file_id: Identifier for this file, which can be used to download or reuse the file
        :param file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        :param width: Photo width
        :param height: Photo height
        :param file_size: Optional. File size
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.file_size = file_size


class Audio:
    """This object represents an audio file to be treated as music by the Telegram clients."""

    def __init__(self, file_id: str, file_unique_id: str, duration: int, performer: Optional[str] = None, title: Optional[str] = None, mime_type: Optional[str] = None, file_size: Optional[int] = None, thumb: Optional[PhotoSize] = None):
        """
        :param file_id: Identifier for this file, which can be used to download or reuse the file
        :param file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        :param duration: Duration of the audio in seconds as defined by sender
        :param performer: Optional. Performer of the audio as defined by sender or by audio tags
        :param title: Optional. Title of the audio as defined by sender or by audio tags
        :param mime_type: Optional. MIME type of the file as defined by sender
        :param file_size: Optional. File size
        :param thumb: Optional. Thumbnail of the album cover to which the music file belongs
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.performer = performer
        self.title = title
        self.mime_type = mime_type
        self.file_size = file_size
        self.thumb = thumb


class Document:
    """This object represents a general file (as opposed to photos, voice messages and audio files)."""

    def __init__(self, file_id: str, file_unique_id: str, thumb: Optional[PhotoSize] = None, file_name: Optional[str] = None, mime_type: Optional[str] = None, file_size: Optional[int] = None):
        """
        :param file_id: Identifier for this file, which can be used to download or reuse the file
        :param file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        :param thumb: Optional. Document thumbnail as defined by sender
        :param file_name: Optional. Original filename as defined by sender
        :param mime_type: Optional. MIME type of the file as defined by sender
        :param file_size: Optional. File size
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size


class Video:
    """This object represents a video file."""

    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int, duration: int, thumb: Optional[PhotoSize] = None, mime_type: Optional[str] = None, file_size: Optional[int] = None):
        """
        :param file_id: Identifier for this file, which can be used to download or reuse the file
        :param file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        :param width: Video width as defined by sender
        :param height: Video height as defined by sender
        :param duration: Duration of the video in seconds as defined by sender
        :param thumb: Optional. Video thumbnail
        :param mime_type: Optional. Mime type of a file as defined by sender
        :param file_size: Optional. File size
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.mime_type = mime_type
        self.file_size = file_size


class Animation:
    """This object represents an animation file (GIF or H.264/MPEG-4 AVC video without sound)."""

    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int, duration: int, thumb: Optional[PhotoSize] = None, file_name: Optional[str] = None, mime_type: Optional[str] = None, file_size: Optional[int] = None):
        """
        :param file_id: Identifier for this file, which can be used to download or reuse the file
        :param file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        :param width: Video width as defined by sender
        :param height: Video height as defined by sender
        :param duration: Duration of the video in seconds as defined by sender
        :param thumb: Optional. Animation thumbnail as defined by sender
        :param file_name: Optional. Original animation filename as defined by sender
        :param mime_type: Optional. MIME type of the file as defined by sender
        :param file_size: Optional. File size
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size


class Voice:
    """This object represents a voice note."""

    def __init__(self, file_id: str, file_unique_id: str, duration: int, mime_type: Optional[str] = None, file_size: Optional[int] = None):
        """
        :param file_id: Identifier for this file, which can be used to download or reuse the file
        :param file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        :param duration: Duration of the audio in seconds as defined by sender
        :param mime_type: Optional. MIME type of the file as defined by sender
        :param file_size: Optional. File size
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.mime_type = mime_type
        self.file_size = file_size


class VideoNote:
    """This object represents a video message (available in Telegram apps as of v.4.0)."""

    def __init__(self, file_id: str, file_unique_id: str, length: int, duration: int, thumb: Optional[PhotoSize] = None, file_size: Optional[int] = None):
        """
        :param file_id: Identifier for this file, which can be used to download or reuse the file
        :param file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        :param length: Video width and height (diameter of the video message) as defined by sender
        :param duration: Duration of the video in seconds as defined by sender
        :param thumb: Optional. Video thumbnail
        :param file_size: Optional. File size
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.length = length
        self.duration = duration
        self.thumb = thumb
        self.file_size = file_size


class Contact:
    """This object represents a phone contact."""

    def __init__(self, phone_number: str, first_name: str, last_name: Optional[str] = None, user_id: Optional[int] = None, vcard: Optional[str] = None):
        """
        :param phone_number: Contact's phone number
        :param first_name: Contact's first name
        :param last_name: Optional. Contact's last name
        :param user_id: Optional. Contact's user identifier in Telegram
        :param vcard: Optional. Additional data about the contact in the form of a vCard
        """
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.vcard = vcard


class Location:
    """This object represents a point on the map."""

    def __init__(self, longitude: float, latitude: float):
        """
        :param longitude: Longitude as defined by sender
        :param latitude: Latitude as defined by sender
        """
        self.longitude = longitude
        self.latitude = latitude


class Venue:
    """This object represents a venue."""

    def __init__(self, location: Location, title: str, address: str, foursquare_id: Optional[str] = None, foursquare_type: Optional[str] = None):
        """
        :param location: Venue location
        :param title: Name of the venue
        :param address: Address of the venue
        :param foursquare_id: Optional. Foursquare identifier of the venue
        :param foursquare_type: Optional. Foursquare type of the venue. (For example, “arts_entertainment/default”, “arts_entertainment/aquarium” or “food/icecream”.)
        """
        self.location = location
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type


class PollOption:
    """This object contains information about one answer option in a poll."""

    def __init__(self, text: str, voter_count: int):
        """
        :param text: Option text, 1-100 characters
        :param voter_count: Number of users that voted for this option
        """
        self.text = text
        self.voter_count = voter_count


class PollAnswer:
    """This object represents an answer of a user in a non-anonymous poll."""

    def __init__(self, poll_id: str, user: User, option_ids: List[int]):
        """
        :param poll_id: Unique poll identifier
        :param user: The user, who changed the answer to the poll
        :param option_ids: 0-based identifiers of answer options, chosen by the user. May be empty if the user retracted their vote.
        """
        self.poll_id = poll_id
        self.user = user
        self.option_ids = option_ids


class Poll:
    """This object contains information about a poll."""

    def __init__(self, id_: str, question: str, options: List[PollOption], total_voter_count: int, is_closed: bool, is_anonymous: bool, type_: str, allows_multiple_answers: bool, correct_option_id: Optional[int] = None):
        """
        :param id_: Unique poll identifier
        :param question: Poll question, 1-255 characters
        :param options: List of poll options
        :param total_voter_count: Total number of users that voted in the poll
        :param is_closed: True, if the poll is closed
        :param is_anonymous: True, if the poll is anonymous
        :param type_: Poll type, currently can be “regular” or “quiz”
        :param allows_multiple_answers: True, if the poll allows multiple answers
        :param correct_option_id: Optional. 0-based identifier of the correct answer option. Available only for polls in the quiz mode, which are closed, or was sent (not forwarded) by the bot or to the private chat with the bot.
        """
        self.id_ = id_
        self.question = question
        self.options = options
        self.total_voter_count = total_voter_count
        self.is_closed = is_closed
        self.is_anonymous = is_anonymous
        self.type_ = type_
        self.allows_multiple_answers = allows_multiple_answers
        self.correct_option_id = correct_option_id


class UserProfilePhotos:
    """This object represent a user's profile pictures."""

    def __init__(self, total_count: int, photos: List[List[PhotoSize]]):
        """
        :param total_count: Total number of profile pictures the target user has
        :param photos: Requested profile pictures (in up to 4 sizes each)
        """
        self.total_count = total_count
        self.photos = photos


class File:
    """This object represents a file ready to be downloaded. The file can be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>. It is guaranteed that the link will be valid for at least 1 hour. When the link expires, a new one can be requested by calling getFile."""


class ReplyKeyboardMarkup:
    """This object represents a custom keyboard with reply options (see Introduction to bots for details and examples)."""

    def __init__(self, keyboard: List[List[KeyboardButton]], resize_keyboard: Optional[bool] = None, one_time_keyboard: Optional[bool] = None, selective: Optional[bool] = None):
        """
        :param keyboard: Array of button rows, each represented by an Array of KeyboardButton objects
        :param resize_keyboard: Optional. Requests clients to resize the keyboard vertically for optimal fit (e.g., make the keyboard smaller if there are just two rows of buttons). Defaults to false, in which case the custom keyboard is always of the same height as the app's standard keyboard.
        :param one_time_keyboard: Optional. Requests clients to hide the keyboard as soon as it's been used. The keyboard will still be available, but clients will automatically display the usual letter-keyboard in the chat – the user can press a special button in the input field to see the custom keyboard again. Defaults to false.
        :param selective: Optional. Use this parameter if you want to show the keyboard to specific users only. Targets: 1) users that are @mentioned in the text of the Message object; 2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.

        Example: A user requests to change the bot‘s language, bot replies to the request with a keyboard to select the new language. Other users in the group don’t see the keyboard.
        """
        self.keyboard = keyboard
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective


class KeyboardButton:
    """This object represents one button of the reply keyboard. For simple text buttons String can be used instead of this object to specify text of the button. Optional fields request_contact, request_location, and request_poll are mutually exclusive."""

    def __init__(self, text: str, request_contact: Optional[bool] = None, request_location: Optional[bool] = None, request_poll: Optional[KeyboardButtonPollType] = None):
        """
        :param text: Text of the button. If none of the optional fields are used, it will be sent as a message when the button is pressed
        :param request_contact: Optional. If True, the user's phone number will be sent as a contact when the button is pressed. Available in private chats only
        :param request_location: Optional. If True, the user's current location will be sent when the button is pressed. Available in private chats only
        :param request_poll: Optional. If specified, the user will be asked to create a poll and send it to the bot when the button is pressed. Available in private chats only
        """
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_poll = request_poll


class KeyboardButtonPollType:
    """This object represents type of a poll, which is allowed to be created and sent when the corresponding button is pressed."""

    def __init__(self, type_: Optional[str] = None):
        """:param type_: Optional. If quiz is passed, the user will be allowed to create only polls in the quiz mode. If regular is passed, only regular polls will be allowed. Otherwise, the user will be allowed to create a poll of any type."""
        self.type_ = type_


class ReplyKeyboardRemove:
    """Upon receiving a message with this object, Telegram clients will remove the current custom keyboard and display the default letter-keyboard. By default, custom keyboards are displayed until a new keyboard is sent by a bot. An exception is made for one-time keyboards that are hidden immediately after the user presses a button (see ReplyKeyboardMarkup)."""

    def __init__(self, remove_keyboard: bool, selective: Optional[bool] = None):
        """
        :param remove_keyboard: Requests clients to remove the custom keyboard (user will not be able to summon this keyboard; if you want to hide the keyboard from sight but keep it accessible, use one_time_keyboard in ReplyKeyboardMarkup)
        :param selective: Optional. Use this parameter if you want to remove the keyboard for specific users only. Targets: 1) users that are @mentioned in the text of the Message object; 2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.

        Example: A user votes in a poll, bot returns confirmation message in reply to the vote and removes the keyboard for that user, while still showing the keyboard with poll options to users who haven't voted yet.
        """
        self.remove_keyboard = remove_keyboard
        self.selective = selective


class InlineKeyboardMarkup:
    """This object represents an inline keyboard that appears right next to the message it belongs to."""

    def __init__(self, inline_keyboard: List[List[InlineKeyboardButton]]):
        """:param inline_keyboard: Array of button rows, each represented by an Array of InlineKeyboardButton objects"""
        self.inline_keyboard = inline_keyboard


class InlineKeyboardButton:
    """This object represents one button of an inline keyboard. You must use exactly one of the optional fields."""

    def __init__(self, text: str, url: Optional[str] = None, login_url: Optional[LoginUrl] = None, callback_data: Optional[str] = None, switch_inline_query: Optional[str] = None, switch_inline_query_current_chat: Optional[str] = None, callback_game: Optional[CallbackGame] = None, pay: Optional[bool] = None):
        """
        :param text: Label text on the button
        :param url: Optional. HTTP or tg:// url to be opened when button is pressed
        :param login_url: Optional. An HTTP URL used to automatically authorize the user. Can be used as a replacement for the Telegram Login Widget.
        :param callback_data: Optional. Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes
        :param switch_inline_query: Optional. If set, pressing the button will prompt the user to select one of their chats, open that chat and insert the bot‘s username and the specified inline query in the input field. Can be empty, in which case just the bot’s username will be inserted.

        Note: This offers an easy way for users to start using your bot in inline mode when they are currently in a private chat with it. Especially useful when combined with switch_pm… actions – in this case the user will be automatically returned to the chat they switched from, skipping the chat selection screen.
        :param switch_inline_query_current_chat: Optional. If set, pressing the button will insert the bot‘s username and the specified inline query in the current chat's input field. Can be empty, in which case only the bot’s username will be inserted.

        This offers a quick way for the user to open your bot in inline mode in the same chat – good for selecting something from multiple options.
        :param callback_game: Optional. Description of the game that will be launched when the user presses the button.

        NOTE: This type of button must always be the first button in the first row.
        :param pay: Optional. Specify True, to send a Pay button.

        NOTE: This type of button must always be the first button in the first row.
        """
        self.text = text
        self.url = url
        self.login_url = login_url
        self.callback_data = callback_data
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        self.pay = pay


class LoginUrl:
    """This object represents a parameter of the inline keyboard button used to automatically authorize a user. Serves as a great replacement for the Telegram Login Widget when the user is coming from Telegram. All the user needs to do is tap/click a button and confirm that they want to log in:"""


class CallbackQuery:
    """This object represents an incoming callback query from a callback button in an inline keyboard. If the button that originated the query was attached to a message sent by the bot, the field message will be present. If the button was attached to a message sent via the bot (in inline mode), the field inline_message_id will be present. Exactly one of the fields data or game_short_name will be present."""

    def __init__(self, id_: str, from_: User, chat_instance: str, message: Optional[Message] = None, inline_message_id: Optional[str] = None, data: Optional[str] = None, game_short_name: Optional[str] = None):
        """
        :param id_: Unique identifier for this query
        :param from_: Sender
        :param message: Optional. Message with the callback button that originated the query. Note that message content and message date will not be available if the message is too old
        :param inline_message_id: Optional. Identifier of the message sent via the bot in inline mode, that originated the query.
        :param chat_instance: Global identifier, uniquely corresponding to the chat to which the message with the callback button was sent. Useful for high scores in games.
        :param data: Optional. Data associated with the callback button. Be aware that a bad client can send arbitrary data in this field.
        :param game_short_name: Optional. Short name of a Game to be returned, serves as the unique identifier for the game
        """
        self.id_ = id_
        self.from_ = from_
        self.message = message
        self.inline_message_id = inline_message_id
        self.chat_instance = chat_instance
        self.data = data
        self.game_short_name = game_short_name


class ForceReply:
    """Upon receiving a message with this object, Telegram clients will display a reply interface to the user (act as if the user has selected the bot‘s message and tapped ’Reply'). This can be extremely useful if you want to create user-friendly step-by-step interfaces without having to sacrifice privacy mode."""

    def __init__(self, force_reply: bool, selective: Optional[bool] = None):
        """
        :param force_reply: Shows reply interface to the user, as if they manually selected the bot‘s message and tapped ’Reply'
        :param selective: Optional. Use this parameter if you want to force reply from specific users only. Targets: 1) users that are @mentioned in the text of the Message object; 2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
        """
        self.force_reply = force_reply
        self.selective = selective


class ChatPhoto:
    """This object represents a chat photo."""

    def __init__(self, small_file_id: str, small_file_unique_id: str, big_file_id: str, big_file_unique_id: str):
        """
        :param small_file_id: File identifier of small (160x160) chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed.
        :param small_file_unique_id: Unique file identifier of small (160x160) chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        :param big_file_id: File identifier of big (640x640) chat photo. This file_id can be used only for photo download and only for as long as the photo is not changed.
        :param big_file_unique_id: Unique file identifier of big (640x640) chat photo, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        """
        self.small_file_id = small_file_id
        self.small_file_unique_id = small_file_unique_id
        self.big_file_id = big_file_id
        self.big_file_unique_id = big_file_unique_id


class ChatMember:
    """This object contains information about one member of a chat."""

    def __init__(self, user: User, status: str, custom_title: Optional[str] = None, until_date: Optional[int] = None, can_be_edited: Optional[bool] = None, can_post_messages: Optional[bool] = None, can_edit_messages: Optional[bool] = None, can_delete_messages: Optional[bool] = None, can_restrict_members: Optional[bool] = None, can_promote_members: Optional[bool] = None, can_change_info: Optional[bool] = None, can_invite_users: Optional[bool] = None, can_pin_messages: Optional[bool] = None, is_member: Optional[bool] = None, can_send_messages: Optional[bool] = None, can_send_media_messages: Optional[bool] = None, can_send_polls: Optional[bool] = None, can_send_other_messages: Optional[bool] = None, can_add_web_page_previews: Optional[bool] = None):
        """
        :param user: Information about the user
        :param status: The member's status in the chat. Can be “creator”, “administrator”, “member”, “restricted”, “left” or “kicked”
        :param custom_title: Optional. Owner and administrators only. Custom title for this user
        :param until_date: Optional. Restricted and kicked only. Date when restrictions will be lifted for this user; unix time
        :param can_be_edited: Optional. Administrators only. True, if the bot is allowed to edit administrator privileges of that user
        :param can_post_messages: Optional. Administrators only. True, if the administrator can post in the channel; channels only
        :param can_edit_messages: Optional. Administrators only. True, if the administrator can edit messages of other users and can pin messages; channels only
        :param can_delete_messages: Optional. Administrators only. True, if the administrator can delete messages of other users
        :param can_restrict_members: Optional. Administrators only. True, if the administrator can restrict, ban or unban chat members
        :param can_promote_members: Optional. Administrators only. True, if the administrator can add new administrators with a subset of his own privileges or demote administrators that he has promoted, directly or indirectly (promoted by administrators that were appointed by the user)
        :param can_change_info: Optional. Administrators and restricted only. True, if the user is allowed to change the chat title, photo and other settings
        :param can_invite_users: Optional. Administrators and restricted only. True, if the user is allowed to invite new users to the chat
        :param can_pin_messages: Optional. Administrators and restricted only. True, if the user is allowed to pin messages; groups and supergroups only
        :param is_member: Optional. Restricted only. True, if the user is a member of the chat at the moment of the request
        :param can_send_messages: Optional. Restricted only. True, if the user is allowed to send text messages, contacts, locations and venues
        :param can_send_media_messages: Optional. Restricted only. True, if the user is allowed to send audios, documents, photos, videos, video notes and voice notes
        :param can_send_polls: Optional. Restricted only. True, if the user is allowed to send polls
        :param can_send_other_messages: Optional. Restricted only. True, if the user is allowed to send animations, games, stickers and use inline bots
        :param can_add_web_page_previews: Optional. Restricted only. True, if the user is allowed to add web page previews to their messages
        """
        self.user = user
        self.status = status
        self.custom_title = custom_title
        self.until_date = until_date
        self.can_be_edited = can_be_edited
        self.can_post_messages = can_post_messages
        self.can_edit_messages = can_edit_messages
        self.can_delete_messages = can_delete_messages
        self.can_restrict_members = can_restrict_members
        self.can_promote_members = can_promote_members
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages
        self.is_member = is_member
        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_polls = can_send_polls
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews


class ChatPermissions:
    """Describes actions that a non-administrator user is allowed to take in a chat."""

    def __init__(self, can_send_messages: Optional[bool] = None, can_send_media_messages: Optional[bool] = None, can_send_polls: Optional[bool] = None, can_send_other_messages: Optional[bool] = None, can_add_web_page_previews: Optional[bool] = None, can_change_info: Optional[bool] = None, can_invite_users: Optional[bool] = None, can_pin_messages: Optional[bool] = None):
        """
        :param can_send_messages: Optional. True, if the user is allowed to send text messages, contacts, locations and venues
        :param can_send_media_messages: Optional. True, if the user is allowed to send audios, documents, photos, videos, video notes and voice notes, implies can_send_messages
        :param can_send_polls: Optional. True, if the user is allowed to send polls, implies can_send_messages
        :param can_send_other_messages: Optional. True, if the user is allowed to send animations, games, stickers and use inline bots, implies can_send_media_messages
        :param can_add_web_page_previews: Optional. True, if the user is allowed to add web page previews to their messages, implies can_send_media_messages
        :param can_change_info: Optional. True, if the user is allowed to change the chat title, photo and other settings. Ignored in public supergroups
        :param can_invite_users: Optional. True, if the user is allowed to invite new users to the chat
        :param can_pin_messages: Optional. True, if the user is allowed to pin messages. Ignored in public supergroups
        """
        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_polls = can_send_polls
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages


class ResponseParameters:
    """Contains information about why a request was unsuccessful."""

    def __init__(self, migrate_to_chat_id: Optional[int] = None, retry_after: Optional[int] = None):
        """
        :param migrate_to_chat_id: Optional. The group has been migrated to a supergroup with the specified identifier. This number may be greater than 32 bits and some programming languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe for storing this identifier.
        :param retry_after: Optional. In case of exceeding flood control, the number of seconds left to wait before the request can be repeated
        """
        self.migrate_to_chat_id = migrate_to_chat_id
        self.retry_after = retry_after


class InputMedia:
    """This object represents the content of a media message to be sent. It should be one of"""


class InputMediaPhoto:
    """Represents a photo to be sent."""

    def __init__(self, type_: str, media: str, caption: Optional[str] = None, parse_mode: Optional[str] = None):
        """
        :param type_: Type of the result, must be photo
        :param media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under <file_attach_name> name. More info on Sending Files »
        :param caption: Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        """
        self.type_ = type_
        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode


class InputMediaVideo:
    """Represents a video to be sent."""

    def __init__(self, type_: str, media: str, thumb: Optional[Union[InputFile, str]] = None, caption: Optional[str] = None, parse_mode: Optional[str] = None, width: Optional[int] = None, height: Optional[int] = None, duration: Optional[int] = None, supports_streaming: Optional[bool] = None):
        """
        :param type_: Type of the result, must be video
        :param media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under <file_attach_name> name. More info on Sending Files »
        :param thumb: Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail‘s width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can’t be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files »
        :param caption: Optional. Caption of the video to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param width: Optional. Video width
        :param height: Optional. Video height
        :param duration: Optional. Video duration
        :param supports_streaming: Optional. Pass True, if the uploaded video is suitable for streaming
        """
        self.type_ = type_
        self.media = media
        self.thumb = thumb
        self.caption = caption
        self.parse_mode = parse_mode
        self.width = width
        self.height = height
        self.duration = duration
        self.supports_streaming = supports_streaming


class InputMediaAnimation:
    """Represents an animation file (GIF or H.264/MPEG-4 AVC video without sound) to be sent."""

    def __init__(self, type_: str, media: str, thumb: Optional[Union[InputFile, str]] = None, caption: Optional[str] = None, parse_mode: Optional[str] = None, width: Optional[int] = None, height: Optional[int] = None, duration: Optional[int] = None):
        """
        :param type_: Type of the result, must be animation
        :param media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under <file_attach_name> name. More info on Sending Files »
        :param thumb: Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail‘s width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can’t be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files »
        :param caption: Optional. Caption of the animation to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param width: Optional. Animation width
        :param height: Optional. Animation height
        :param duration: Optional. Animation duration
        """
        self.type_ = type_
        self.media = media
        self.thumb = thumb
        self.caption = caption
        self.parse_mode = parse_mode
        self.width = width
        self.height = height
        self.duration = duration


class InputMediaAudio:
    """Represents an audio file to be treated as music to be sent."""

    def __init__(self, type_: str, media: str, thumb: Optional[Union[InputFile, str]] = None, caption: Optional[str] = None, parse_mode: Optional[str] = None, duration: Optional[int] = None, performer: Optional[str] = None, title: Optional[str] = None):
        """
        :param type_: Type of the result, must be audio
        :param media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under <file_attach_name> name. More info on Sending Files »
        :param thumb: Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail‘s width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can’t be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files »
        :param caption: Optional. Caption of the audio to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param duration: Optional. Duration of the audio in seconds
        :param performer: Optional. Performer of the audio
        :param title: Optional. Title of the audio
        """
        self.type_ = type_
        self.media = media
        self.thumb = thumb
        self.caption = caption
        self.parse_mode = parse_mode
        self.duration = duration
        self.performer = performer
        self.title = title


class InputMediaDocument:
    """Represents a general file to be sent."""

    def __init__(self, type_: str, media: str, thumb: Optional[Union[InputFile, str]] = None, caption: Optional[str] = None, parse_mode: Optional[str] = None):
        """
        :param type_: Type of the result, must be document
        :param media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>” to upload a new one using multipart/form-data under <file_attach_name> name. More info on Sending Files »
        :param thumb: Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail‘s width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can’t be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded using multipart/form-data under <file_attach_name>. More info on Sending Files »
        :param caption: Optional. Caption of the document to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        """
        self.type_ = type_
        self.media = media
        self.thumb = thumb
        self.caption = caption
        self.parse_mode = parse_mode


class InputFile:
    """This object represents the contents of a file to be uploaded. Must be posted using multipart/form-data in the usual way that files are uploaded via the browser."""


class Sticker:
    """This object represents a sticker."""

    def __init__(self, file_id: str, file_unique_id: str, width: int, height: int, is_animated: bool, thumb: Optional[PhotoSize] = None, emoji: Optional[str] = None, set_name: Optional[str] = None, mask_position: Optional[MaskPosition] = None, file_size: Optional[int] = None):
        """
        :param file_id: Identifier for this file, which can be used to download or reuse the file
        :param file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        :param width: Sticker width
        :param height: Sticker height
        :param is_animated: True, if the sticker is animated
        :param thumb: Optional. Sticker thumbnail in the .webp or .jpg format
        :param emoji: Optional. Emoji associated with the sticker
        :param set_name: Optional. Name of the sticker set to which the sticker belongs
        :param mask_position: Optional. For mask stickers, the position where the mask should be placed
        :param file_size: Optional. File size
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.is_animated = is_animated
        self.thumb = thumb
        self.emoji = emoji
        self.set_name = set_name
        self.mask_position = mask_position
        self.file_size = file_size


class StickerSet:
    """This object represents a sticker set."""

    def __init__(self, name: str, title: str, is_animated: bool, contains_masks: bool, stickers: List[Sticker]):
        """
        :param name: Sticker set name
        :param title: Sticker set title
        :param is_animated: True, if the sticker set contains animated stickers
        :param contains_masks: True, if the sticker set contains masks
        :param stickers: List of all set stickers
        """
        self.name = name
        self.title = title
        self.is_animated = is_animated
        self.contains_masks = contains_masks
        self.stickers = stickers


class MaskPosition:
    """This object describes the position on faces where a mask should be placed by default."""

    def __init__(self, point: str, x_shift: float, y_shift: float, scale: float):
        """
        :param point: The part of the face relative to which the mask should be placed. One of “forehead”, “eyes”, “mouth”, or “chin”.
        :param x_shift: Shift by X-axis measured in widths of the mask scaled to the face size, from left to right. For example, choosing -1.0 will place mask just to the left of the default mask position.
        :param y_shift: Shift by Y-axis measured in heights of the mask scaled to the face size, from top to bottom. For example, 1.0 will place the mask just below the default mask position.
        :param scale: Mask scaling coefficient. For example, 2.0 means double size.
        """
        self.point = point
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.scale = scale


class InlineQuery:
    """This object represents an incoming inline query. When the user sends an empty query, your bot could return some default or trending results."""

    def __init__(self, id_: str, from_: User, query: str, offset: str, location: Optional[Location] = None):
        """
        :param id_: Unique identifier for this query
        :param from_: Sender
        :param location: Optional. Sender location, only for bots that request user location
        :param query: Text of the query (up to 256 characters)
        :param offset: Offset of the results to be returned, can be controlled by the bot
        """
        self.id_ = id_
        self.from_ = from_
        self.location = location
        self.query = query
        self.offset = offset


class InlineQueryResult:
    """This object represents one result of an inline query. Telegram clients currently support results of the following 20 types:"""


class InlineQueryResultArticle:
    """Represents a link to an article or web page."""

    def __init__(self, type_: str, id_: str, title: str, input_message_content: InputMessageContent, reply_markup: Optional[InlineKeyboardMarkup] = None, url: Optional[str] = None, hide_url: Optional[bool] = None, description: Optional[str] = None, thumb_url: Optional[str] = None, thumb_width: Optional[int] = None, thumb_height: Optional[int] = None):
        """
        :param type_: Type of the result, must be article
        :param id_: Unique identifier for this result, 1-64 Bytes
        :param title: Title of the result
        :param input_message_content: Content of the message to be sent
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param url: Optional. URL of the result
        :param hide_url: Optional. Pass True, if you don't want the URL to be shown in the message
        :param description: Optional. Short description of the result
        :param thumb_url: Optional. Url of the thumbnail for the result
        :param thumb_width: Optional. Thumbnail width
        :param thumb_height: Optional. Thumbnail height
        """
        self.type_ = type_
        self.id_ = id_
        self.title = title
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup
        self.url = url
        self.hide_url = hide_url
        self.description = description
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height


class InlineQueryResultPhoto:
    """Represents a link to a photo. By default, this photo will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the photo."""

    def __init__(self, type_: str, id_: str, photo_url: str, thumb_url: str, photo_width: Optional[int] = None, photo_height: Optional[int] = None, title: Optional[str] = None, description: Optional[str] = None, caption: Optional[str] = None, parse_mode: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be photo
        :param id_: Unique identifier for this result, 1-64 bytes
        :param photo_url: A valid URL of the photo. Photo must be in jpeg format. Photo size must not exceed 5MB
        :param thumb_url: URL of the thumbnail for the photo
        :param photo_width: Optional. Width of the photo
        :param photo_height: Optional. Height of the photo
        :param title: Optional. Title for the result
        :param description: Optional. Short description of the result
        :param caption: Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the photo
        """
        self.type_ = type_
        self.id_ = id_
        self.photo_url = photo_url
        self.thumb_url = thumb_url
        self.photo_width = photo_width
        self.photo_height = photo_height
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InlineQueryResultGif:
    """Represents a link to an animated GIF file. By default, this animated GIF file will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation."""

    def __init__(self, type_: str, id_: str, gif_url: str, thumb_url: str, gif_width: Optional[int] = None, gif_height: Optional[int] = None, gif_duration: Optional[int] = None, title: Optional[str] = None, caption: Optional[str] = None, parse_mode: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be gif
        :param id_: Unique identifier for this result, 1-64 bytes
        :param gif_url: A valid URL for the GIF file. File size must not exceed 1MB
        :param gif_width: Optional. Width of the GIF
        :param gif_height: Optional. Height of the GIF
        :param gif_duration: Optional. Duration of the GIF
        :param thumb_url: URL of the static thumbnail for the result (jpeg or gif)
        :param title: Optional. Title for the result
        :param caption: Optional. Caption of the GIF file to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the GIF animation
        """
        self.type_ = type_
        self.id_ = id_
        self.gif_url = gif_url
        self.gif_width = gif_width
        self.gif_height = gif_height
        self.gif_duration = gif_duration
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InlineQueryResultMpeg4Gif:
    """Represents a link to a video animation (H.264/MPEG-4 AVC video without sound). By default, this animated MPEG-4 file will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation."""

    def __init__(self, type_: str, id_: str, mpeg4_url: str, thumb_url: str, mpeg4_width: Optional[int] = None, mpeg4_height: Optional[int] = None, mpeg4_duration: Optional[int] = None, title: Optional[str] = None, caption: Optional[str] = None, parse_mode: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be mpeg4_gif
        :param id_: Unique identifier for this result, 1-64 bytes
        :param mpeg4_url: A valid URL for the MP4 file. File size must not exceed 1MB
        :param mpeg4_width: Optional. Video width
        :param mpeg4_height: Optional. Video height
        :param mpeg4_duration: Optional. Video duration
        :param thumb_url: URL of the static thumbnail (jpeg or gif) for the result
        :param title: Optional. Title for the result
        :param caption: Optional. Caption of the MPEG-4 file to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the video animation
        """
        self.type_ = type_
        self.id_ = id_
        self.mpeg4_url = mpeg4_url
        self.mpeg4_width = mpeg4_width
        self.mpeg4_height = mpeg4_height
        self.mpeg4_duration = mpeg4_duration
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InlineQueryResultVideo:
    """Represents a link to a page containing an embedded video player or a video file. By default, this video file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the video."""


class InlineQueryResultAudio:
    """Represents a link to an MP3 audio file. By default, this audio file will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the audio."""

    def __init__(self, type_: str, id_: str, audio_url: str, title: str, caption: Optional[str] = None, parse_mode: Optional[str] = None, performer: Optional[str] = None, audio_duration: Optional[int] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be audio
        :param id_: Unique identifier for this result, 1-64 bytes
        :param audio_url: A valid URL for the audio file
        :param title: Title
        :param caption: Optional. Caption, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param performer: Optional. Performer
        :param audio_duration: Optional. Audio duration in seconds
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the audio
        """
        self.type_ = type_
        self.id_ = id_
        self.audio_url = audio_url
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.performer = performer
        self.audio_duration = audio_duration
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InlineQueryResultVoice:
    """Represents a link to a voice recording in an .ogg container encoded with OPUS. By default, this voice recording will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the the voice message."""

    def __init__(self, type_: str, id_: str, voice_url: str, title: str, caption: Optional[str] = None, parse_mode: Optional[str] = None, voice_duration: Optional[int] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be voice
        :param id_: Unique identifier for this result, 1-64 bytes
        :param voice_url: A valid URL for the voice recording
        :param title: Recording title
        :param caption: Optional. Caption, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param voice_duration: Optional. Recording duration in seconds
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the voice recording
        """
        self.type_ = type_
        self.id_ = id_
        self.voice_url = voice_url
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.voice_duration = voice_duration
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InlineQueryResultDocument:
    """Represents a link to a file. By default, this file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the file. Currently, only .PDF and .ZIP files can be sent using this method."""

    def __init__(self, type_: str, id_: str, title: str, document_url: str, mime_type: str, caption: Optional[str] = None, parse_mode: Optional[str] = None, description: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None, thumb_url: Optional[str] = None, thumb_width: Optional[int] = None, thumb_height: Optional[int] = None):
        """
        :param type_: Type of the result, must be document
        :param id_: Unique identifier for this result, 1-64 bytes
        :param title: Title for the result
        :param caption: Optional. Caption of the document to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param document_url: A valid URL for the file
        :param mime_type: Mime type of the content of the file, either “application/pdf” or “application/zip”
        :param description: Optional. Short description of the result
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the file
        :param thumb_url: Optional. URL of the thumbnail (jpeg only) for the file
        :param thumb_width: Optional. Thumbnail width
        :param thumb_height: Optional. Thumbnail height
        """
        self.type_ = type_
        self.id_ = id_
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.document_url = document_url
        self.mime_type = mime_type
        self.description = description
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height


class InlineQueryResultLocation:
    """Represents a location on a map. By default, the location will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the location."""

    def __init__(self, type_: str, id_: str, latitude: float, longitude: float, title: str, live_period: Optional[int] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None, thumb_url: Optional[str] = None, thumb_width: Optional[int] = None, thumb_height: Optional[int] = None):
        """
        :param type_: Type of the result, must be location
        :param id_: Unique identifier for this result, 1-64 Bytes
        :param latitude: Location latitude in degrees
        :param longitude: Location longitude in degrees
        :param title: Location title
        :param live_period: Optional. Period in seconds for which the location can be updated, should be between 60 and 86400.
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the location
        :param thumb_url: Optional. Url of the thumbnail for the result
        :param thumb_width: Optional. Thumbnail width
        :param thumb_height: Optional. Thumbnail height
        """
        self.type_ = type_
        self.id_ = id_
        self.latitude = latitude
        self.longitude = longitude
        self.title = title
        self.live_period = live_period
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height


class InlineQueryResultVenue:
    """Represents a venue. By default, the venue will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the venue."""

    def __init__(self, type_: str, id_: str, latitude: float, longitude: float, title: str, address: str, foursquare_id: Optional[str] = None, foursquare_type: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None, thumb_url: Optional[str] = None, thumb_width: Optional[int] = None, thumb_height: Optional[int] = None):
        """
        :param type_: Type of the result, must be venue
        :param id_: Unique identifier for this result, 1-64 Bytes
        :param latitude: Latitude of the venue location in degrees
        :param longitude: Longitude of the venue location in degrees
        :param title: Title of the venue
        :param address: Address of the venue
        :param foursquare_id: Optional. Foursquare identifier of the venue if known
        :param foursquare_type: Optional. Foursquare type of the venue, if known. (For example, “arts_entertainment/default”, “arts_entertainment/aquarium” or “food/icecream”.)
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the venue
        :param thumb_url: Optional. Url of the thumbnail for the result
        :param thumb_width: Optional. Thumbnail width
        :param thumb_height: Optional. Thumbnail height
        """
        self.type_ = type_
        self.id_ = id_
        self.latitude = latitude
        self.longitude = longitude
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height


class InlineQueryResultContact:
    """Represents a contact with a phone number. By default, this contact will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the contact."""

    def __init__(self, type_: str, id_: str, phone_number: str, first_name: str, last_name: Optional[str] = None, vcard: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None, thumb_url: Optional[str] = None, thumb_width: Optional[int] = None, thumb_height: Optional[int] = None):
        """
        :param type_: Type of the result, must be contact
        :param id_: Unique identifier for this result, 1-64 Bytes
        :param phone_number: Contact's phone number
        :param first_name: Contact's first name
        :param last_name: Optional. Contact's last name
        :param vcard: Optional. Additional data about the contact in the form of a vCard, 0-2048 bytes
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the contact
        :param thumb_url: Optional. Url of the thumbnail for the result
        :param thumb_width: Optional. Thumbnail width
        :param thumb_height: Optional. Thumbnail height
        """
        self.type_ = type_
        self.id_ = id_
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.vcard = vcard
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height


class InlineQueryResultGame:
    """Represents a Game."""

    def __init__(self, type_: str, id_: str, game_short_name: str, reply_markup: Optional[InlineKeyboardMarkup] = None):
        """
        :param type_: Type of the result, must be game
        :param id_: Unique identifier for this result, 1-64 bytes
        :param game_short_name: Short name of the game
        :param reply_markup: Optional. Inline keyboard attached to the message
        """
        self.type_ = type_
        self.id_ = id_
        self.game_short_name = game_short_name
        self.reply_markup = reply_markup


class InlineQueryResultCachedPhoto:
    """Represents a link to a photo stored on the Telegram servers. By default, this photo will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the photo."""

    def __init__(self, type_: str, id_: str, photo_file_id: str, title: Optional[str] = None, description: Optional[str] = None, caption: Optional[str] = None, parse_mode: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be photo
        :param id_: Unique identifier for this result, 1-64 bytes
        :param photo_file_id: A valid file identifier of the photo
        :param title: Optional. Title for the result
        :param description: Optional. Short description of the result
        :param caption: Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the photo
        """
        self.type_ = type_
        self.id_ = id_
        self.photo_file_id = photo_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InlineQueryResultCachedGif:
    """Represents a link to an animated GIF file stored on the Telegram servers. By default, this animated GIF file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with specified content instead of the animation."""

    def __init__(self, type_: str, id_: str, gif_file_id: str, title: Optional[str] = None, caption: Optional[str] = None, parse_mode: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be gif
        :param id_: Unique identifier for this result, 1-64 bytes
        :param gif_file_id: A valid file identifier for the GIF file
        :param title: Optional. Title for the result
        :param caption: Optional. Caption of the GIF file to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the GIF animation
        """
        self.type_ = type_
        self.id_ = id_
        self.gif_file_id = gif_file_id
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InlineQueryResultCachedMpeg4Gif:
    """Represents a link to a video animation (H.264/MPEG-4 AVC video without sound) stored on the Telegram servers. By default, this animated MPEG-4 file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation."""

    def __init__(self, type_: str, id_: str, mpeg4_file_id: str, title: Optional[str] = None, caption: Optional[str] = None, parse_mode: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be mpeg4_gif
        :param id_: Unique identifier for this result, 1-64 bytes
        :param mpeg4_file_id: A valid file identifier for the MP4 file
        :param title: Optional. Title for the result
        :param caption: Optional. Caption of the MPEG-4 file to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the video animation
        """
        self.type_ = type_
        self.id_ = id_
        self.mpeg4_file_id = mpeg4_file_id
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InlineQueryResultCachedSticker:
    """Represents a link to a sticker stored on the Telegram servers. By default, this sticker will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the sticker."""

    def __init__(self, type_: str, id_: str, sticker_file_id: str, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be sticker
        :param id_: Unique identifier for this result, 1-64 bytes
        :param sticker_file_id: A valid file identifier of the sticker
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the sticker
        """
        self.type_ = type_
        self.id_ = id_
        self.sticker_file_id = sticker_file_id
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InlineQueryResultCachedDocument:
    """Represents a link to a file stored on the Telegram servers. By default, this file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the file."""

    def __init__(self, type_: str, id_: str, title: str, document_file_id: str, description: Optional[str] = None, caption: Optional[str] = None, parse_mode: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be document
        :param id_: Unique identifier for this result, 1-64 bytes
        :param title: Title for the result
        :param document_file_id: A valid file identifier for the file
        :param description: Optional. Short description of the result
        :param caption: Optional. Caption of the document to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the file
        """
        self.type_ = type_
        self.id_ = id_
        self.title = title
        self.document_file_id = document_file_id
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InlineQueryResultCachedVideo:
    """Represents a link to a video file stored on the Telegram servers. By default, this video file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the video."""

    def __init__(self, type_: str, id_: str, video_file_id: str, title: str, description: Optional[str] = None, caption: Optional[str] = None, parse_mode: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be video
        :param id_: Unique identifier for this result, 1-64 bytes
        :param video_file_id: A valid file identifier for the video file
        :param title: Title for the result
        :param description: Optional. Short description of the result
        :param caption: Optional. Caption of the video to be sent, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the video
        """
        self.type_ = type_
        self.id_ = id_
        self.video_file_id = video_file_id
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InlineQueryResultCachedVoice:
    """Represents a link to a voice message stored on the Telegram servers. By default, this voice message will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the voice message."""

    def __init__(self, type_: str, id_: str, voice_file_id: str, title: str, caption: Optional[str] = None, parse_mode: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be voice
        :param id_: Unique identifier for this result, 1-64 bytes
        :param voice_file_id: A valid file identifier for the voice message
        :param title: Voice message title
        :param caption: Optional. Caption, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the voice message
        """
        self.type_ = type_
        self.id_ = id_
        self.voice_file_id = voice_file_id
        self.title = title
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InlineQueryResultCachedAudio:
    """Represents a link to an MP3 audio file stored on the Telegram servers. By default, this audio file will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the audio."""

    def __init__(self, type_: str, id_: str, audio_file_id: str, caption: Optional[str] = None, parse_mode: Optional[str] = None, reply_markup: Optional[InlineKeyboardMarkup] = None, input_message_content: Optional[InputMessageContent] = None):
        """
        :param type_: Type of the result, must be audio
        :param id_: Unique identifier for this result, 1-64 bytes
        :param audio_file_id: A valid file identifier for the audio file
        :param caption: Optional. Caption, 0-1024 characters after entities parsing
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.
        :param reply_markup: Optional. Inline keyboard attached to the message
        :param input_message_content: Optional. Content of the message to be sent instead of the audio
        """
        self.type_ = type_
        self.id_ = id_
        self.audio_file_id = audio_file_id
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content


class InputMessageContent:
    """This object represents the content of a message to be sent as a result of an inline query. Telegram clients currently support the following 4 types:"""


class InputTextMessageContent:
    """Represents the content of a text message to be sent as the result of an inline query."""

    def __init__(self, message_text: str, parse_mode: Optional[str] = None, disable_web_page_preview: Optional[bool] = None):
        """
        :param message_text: Text of the message to be sent, 1-4096 characters
        :param parse_mode: Optional. Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your bot's message.
        :param disable_web_page_preview: Optional. Disables link previews for links in the sent message
        """
        self.message_text = message_text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview


class InputLocationMessageContent:
    """Represents the content of a location message to be sent as the result of an inline query."""

    def __init__(self, latitude: float, longitude: float, live_period: Optional[int] = None):
        """
        :param latitude: Latitude of the location in degrees
        :param longitude: Longitude of the location in degrees
        :param live_period: Optional. Period in seconds for which the location can be updated, should be between 60 and 86400.
        """
        self.latitude = latitude
        self.longitude = longitude
        self.live_period = live_period


class InputVenueMessageContent:
    """Represents the content of a venue message to be sent as the result of an inline query."""

    def __init__(self, latitude: float, longitude: float, title: str, address: str, foursquare_id: Optional[str] = None, foursquare_type: Optional[str] = None):
        """
        :param latitude: Latitude of the venue in degrees
        :param longitude: Longitude of the venue in degrees
        :param title: Name of the venue
        :param address: Address of the venue
        :param foursquare_id: Optional. Foursquare identifier of the venue, if known
        :param foursquare_type: Optional. Foursquare type of the venue, if known. (For example, “arts_entertainment/default”, “arts_entertainment/aquarium” or “food/icecream”.)
        """
        self.latitude = latitude
        self.longitude = longitude
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type


class InputContactMessageContent:
    """Represents the content of a contact message to be sent as the result of an inline query."""

    def __init__(self, phone_number: str, first_name: str, last_name: Optional[str] = None, vcard: Optional[str] = None):
        """
        :param phone_number: Contact's phone number
        :param first_name: Contact's first name
        :param last_name: Optional. Contact's last name
        :param vcard: Optional. Additional data about the contact in the form of a vCard, 0-2048 bytes
        """
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.vcard = vcard


class ChosenInlineResult:
    """Represents a result of an inline query that was chosen by the user and sent to their chat partner."""

    def __init__(self, result_id: str, from_: User, query: str, location: Optional[Location] = None, inline_message_id: Optional[str] = None):
        """
        :param result_id: The unique identifier for the result that was chosen
        :param from_: The user that chose the result
        :param location: Optional. Sender location, only for bots that require user location
        :param inline_message_id: Optional. Identifier of the sent inline message. Available only if there is an inline keyboard attached to the message. Will be also received in callback queries and can be used to edit the message.
        :param query: The query that was used to obtain the result
        """
        self.result_id = result_id
        self.from_ = from_
        self.location = location
        self.inline_message_id = inline_message_id
        self.query = query


class LabeledPrice:
    """This object represents a portion of the price for goods or services."""

    def __init__(self, label: str, amount: int):
        """
        :param label: Portion label
        :param amount: Price of the product in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
        """
        self.label = label
        self.amount = amount


class Invoice:
    """This object contains basic information about an invoice."""

    def __init__(self, title: str, description: str, start_parameter: str, currency: str, total_amount: int):
        """
        :param title: Product name
        :param description: Product description
        :param start_parameter: Unique bot deep-linking parameter that can be used to generate this invoice
        :param currency: Three-letter ISO 4217 currency code
        :param total_amount: Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
        """
        self.title = title
        self.description = description
        self.start_parameter = start_parameter
        self.currency = currency
        self.total_amount = total_amount


class ShippingAddress:
    """This object represents a shipping address."""

    def __init__(self, country_code: str, state: str, city: str, street_line1: str, street_line2: str, post_code: str):
        """
        :param country_code: ISO 3166-1 alpha-2 country code
        :param state: State, if applicable
        :param city: City
        :param street_line1: First line for the address
        :param street_line2: Second line for the address
        :param post_code: Address post code
        """
        self.country_code = country_code
        self.state = state
        self.city = city
        self.street_line1 = street_line1
        self.street_line2 = street_line2
        self.post_code = post_code


class OrderInfo:
    """This object represents information about an order."""

    def __init__(self, name: Optional[str] = None, phone_number: Optional[str] = None, email: Optional[str] = None, shipping_address: Optional[ShippingAddress] = None):
        """
        :param name: Optional. User name
        :param phone_number: Optional. User's phone number
        :param email: Optional. User email
        :param shipping_address: Optional. User shipping address
        """
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.shipping_address = shipping_address


class ShippingOption:
    """This object represents one shipping option."""

    def __init__(self, id_: str, title: str, prices: List[LabeledPrice]):
        """
        :param id_: Shipping option identifier
        :param title: Option title
        :param prices: List of price portions
        """
        self.id_ = id_
        self.title = title
        self.prices = prices


class SuccessfulPayment:
    """This object contains basic information about a successful payment."""

    def __init__(self, currency: str, total_amount: int, invoice_payload: str, telegram_payment_charge_id: str, provider_payment_charge_id: str, shipping_option_id: Optional[str] = None, order_info: Optional[OrderInfo] = None):
        """
        :param currency: Three-letter ISO 4217 currency code
        :param total_amount: Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
        :param invoice_payload: Bot specified invoice payload
        :param shipping_option_id: Optional. Identifier of the shipping option chosen by the user
        :param order_info: Optional. Order info provided by the user
        :param telegram_payment_charge_id: Telegram payment identifier
        :param provider_payment_charge_id: Provider payment identifier
        """
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id


class ShippingQuery:
    """This object contains information about an incoming shipping query."""

    def __init__(self, id_: str, from_: User, invoice_payload: str, shipping_address: ShippingAddress):
        """
        :param id_: Unique query identifier
        :param from_: User who sent the query
        :param invoice_payload: Bot specified invoice payload
        :param shipping_address: User specified shipping address
        """
        self.id_ = id_
        self.from_ = from_
        self.invoice_payload = invoice_payload
        self.shipping_address = shipping_address


class PreCheckoutQuery:
    """This object contains information about an incoming pre-checkout query."""

    def __init__(self, id_: str, from_: User, currency: str, total_amount: int, invoice_payload: str, shipping_option_id: Optional[str] = None, order_info: Optional[OrderInfo] = None):
        """
        :param id_: Unique query identifier
        :param from_: User who sent the query
        :param currency: Three-letter ISO 4217 currency code
        :param total_amount: Total price in the smallest units of the currency (integer, not float/double). For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
        :param invoice_payload: Bot specified invoice payload
        :param shipping_option_id: Optional. Identifier of the shipping option chosen by the user
        :param order_info: Optional. Order info provided by the user
        """
        self.id_ = id_
        self.from_ = from_
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.shipping_option_id = shipping_option_id
        self.order_info = order_info


class PassportData:
    """Contains information about Telegram Passport data shared with the bot by the user."""

    def __init__(self, data: List[EncryptedPassportElement], credentials: EncryptedCredentials):
        """
        :param data: Array with information about documents and other Telegram Passport elements that was shared with the bot
        :param credentials: Encrypted credentials required to decrypt the data
        """
        self.data = data
        self.credentials = credentials


class PassportFile:
    """This object represents a file uploaded to Telegram Passport. Currently all Telegram Passport files are in JPEG format when decrypted and don't exceed 10MB."""

    def __init__(self, file_id: str, file_unique_id: str, file_size: int, file_date: int):
        """
        :param file_id: Identifier for this file, which can be used to download or reuse the file
        :param file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
        :param file_size: File size
        :param file_date: Unix time when the file was uploaded
        """
        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_size = file_size
        self.file_date = file_date


class EncryptedPassportElement:
    """Contains information about documents or other Telegram Passport elements shared with the bot by the user."""

    def __init__(self, type_: str, hash_: str, data: Optional[str] = None, phone_number: Optional[str] = None, email: Optional[str] = None, files: Optional[List[PassportFile]] = None, front_side: Optional[PassportFile] = None, reverse_side: Optional[PassportFile] = None, selfie: Optional[PassportFile] = None, translation: Optional[List[PassportFile]] = None):
        """
        :param type_: Element type. One of “personal_details”, “passport”, “driver_license”, “identity_card”, “internal_passport”, “address”, “utility_bill”, “bank_statement”, “rental_agreement”, “passport_registration”, “temporary_registration”, “phone_number”, “email”.
        :param data: Optional. Base64-encoded encrypted Telegram Passport element data provided by the user, available for “personal_details”, “passport”, “driver_license”, “identity_card”, “internal_passport” and “address” types. Can be decrypted and verified using the accompanying EncryptedCredentials.
        :param phone_number: Optional. User's verified phone number, available only for “phone_number” type
        :param email: Optional. User's verified email address, available only for “email” type
        :param files: Optional. Array of encrypted files with documents provided by the user, available for “utility_bill”, “bank_statement”, “rental_agreement”, “passport_registration” and “temporary_registration” types. Files can be decrypted and verified using the accompanying EncryptedCredentials.
        :param front_side: Optional. Encrypted file with the front side of the document, provided by the user. Available for “passport”, “driver_license”, “identity_card” and “internal_passport”. The file can be decrypted and verified using the accompanying EncryptedCredentials.
        :param reverse_side: Optional. Encrypted file with the reverse side of the document, provided by the user. Available for “driver_license” and “identity_card”. The file can be decrypted and verified using the accompanying EncryptedCredentials.
        :param selfie: Optional. Encrypted file with the selfie of the user holding a document, provided by the user; available for “passport”, “driver_license”, “identity_card” and “internal_passport”. The file can be decrypted and verified using the accompanying EncryptedCredentials.
        :param translation: Optional. Array of encrypted files with translated versions of documents provided by the user. Available if requested for “passport”, “driver_license”, “identity_card”, “internal_passport”, “utility_bill”, “bank_statement”, “rental_agreement”, “passport_registration” and “temporary_registration” types. Files can be decrypted and verified using the accompanying EncryptedCredentials.
        :param hash_: Base64-encoded element hash for using in PassportElementErrorUnspecified
        """
        self.type_ = type_
        self.data = data
        self.phone_number = phone_number
        self.email = email
        self.files = files
        self.front_side = front_side
        self.reverse_side = reverse_side
        self.selfie = selfie
        self.translation = translation
        self.hash_ = hash_


class EncryptedCredentials:
    """Contains data required for decrypting and authenticating EncryptedPassportElement. See the Telegram Passport Documentation for a complete description of the data decryption and authentication processes."""

    def __init__(self, data: str, hash_: str, secret: str):
        """
        :param data: Base64-encoded encrypted JSON-serialized data with unique user's payload, data hashes and secrets required for EncryptedPassportElement decryption and authentication
        :param hash_: Base64-encoded data hash for data authentication
        :param secret: Base64-encoded secret, encrypted with the bot's public RSA key, required for data decryption
        """
        self.data = data
        self.hash_ = hash_
        self.secret = secret


class PassportElementError:
    """This object represents an error in the Telegram Passport element which was submitted that should be resolved by the user. It should be one of:"""


class PassportElementErrorDataField:
    """Represents an issue in one of the data fields that was provided by the user. The error is considered resolved when the field's value changes."""

    def __init__(self, source: str, type_: str, field_name: str, data_hash: str, message: str):
        """
        :param source: Error source, must be data
        :param type_: The section of the user's Telegram Passport which has the error, one of “personal_details”, “passport”, “driver_license”, “identity_card”, “internal_passport”, “address”
        :param field_name: Name of the data field which has the error
        :param data_hash: Base64-encoded data hash
        :param message: Error message
        """
        self.source = source
        self.type_ = type_
        self.field_name = field_name
        self.data_hash = data_hash
        self.message = message


class PassportElementErrorFrontSide:
    """Represents an issue with the front side of a document. The error is considered resolved when the file with the front side of the document changes."""

    def __init__(self, source: str, type_: str, file_hash: str, message: str):
        """
        :param source: Error source, must be front_side
        :param type_: The section of the user's Telegram Passport which has the issue, one of “passport”, “driver_license”, “identity_card”, “internal_passport”
        :param file_hash: Base64-encoded hash of the file with the front side of the document
        :param message: Error message
        """
        self.source = source
        self.type_ = type_
        self.file_hash = file_hash
        self.message = message


class PassportElementErrorReverseSide:
    """Represents an issue with the reverse side of a document. The error is considered resolved when the file with reverse side of the document changes."""

    def __init__(self, source: str, type_: str, file_hash: str, message: str):
        """
        :param source: Error source, must be reverse_side
        :param type_: The section of the user's Telegram Passport which has the issue, one of “driver_license”, “identity_card”
        :param file_hash: Base64-encoded hash of the file with the reverse side of the document
        :param message: Error message
        """
        self.source = source
        self.type_ = type_
        self.file_hash = file_hash
        self.message = message


class PassportElementErrorSelfie:
    """Represents an issue with the selfie with a document. The error is considered resolved when the file with the selfie changes."""

    def __init__(self, source: str, type_: str, file_hash: str, message: str):
        """
        :param source: Error source, must be selfie
        :param type_: The section of the user's Telegram Passport which has the issue, one of “passport”, “driver_license”, “identity_card”, “internal_passport”
        :param file_hash: Base64-encoded hash of the file with the selfie
        :param message: Error message
        """
        self.source = source
        self.type_ = type_
        self.file_hash = file_hash
        self.message = message


class PassportElementErrorFile:
    """Represents an issue with a document scan. The error is considered resolved when the file with the document scan changes."""

    def __init__(self, source: str, type_: str, file_hash: str, message: str):
        """
        :param source: Error source, must be file
        :param type_: The section of the user's Telegram Passport which has the issue, one of “utility_bill”, “bank_statement”, “rental_agreement”, “passport_registration”, “temporary_registration”
        :param file_hash: Base64-encoded file hash
        :param message: Error message
        """
        self.source = source
        self.type_ = type_
        self.file_hash = file_hash
        self.message = message


class PassportElementErrorFiles:
    """Represents an issue with a list of scans. The error is considered resolved when the list of files containing the scans changes."""

    def __init__(self, source: str, type_: str, file_hashes: List[str], message: str):
        """
        :param source: Error source, must be files
        :param type_: The section of the user's Telegram Passport which has the issue, one of “utility_bill”, “bank_statement”, “rental_agreement”, “passport_registration”, “temporary_registration”
        :param file_hashes: List of base64-encoded file hashes
        :param message: Error message
        """
        self.source = source
        self.type_ = type_
        self.file_hashes = file_hashes
        self.message = message


class PassportElementErrorTranslationFile:
    """Represents an issue with one of the files that constitute the translation of a document. The error is considered resolved when the file changes."""

    def __init__(self, source: str, type_: str, file_hash: str, message: str):
        """
        :param source: Error source, must be translation_file
        :param type_: Type of element of the user's Telegram Passport which has the issue, one of “passport”, “driver_license”, “identity_card”, “internal_passport”, “utility_bill”, “bank_statement”, “rental_agreement”, “passport_registration”, “temporary_registration”
        :param file_hash: Base64-encoded file hash
        :param message: Error message
        """
        self.source = source
        self.type_ = type_
        self.file_hash = file_hash
        self.message = message


class PassportElementErrorTranslationFiles:
    """Represents an issue with the translated version of a document. The error is considered resolved when a file with the document translation change."""

    def __init__(self, source: str, type_: str, file_hashes: List[str], message: str):
        """
        :param source: Error source, must be translation_files
        :param type_: Type of element of the user's Telegram Passport which has the issue, one of “passport”, “driver_license”, “identity_card”, “internal_passport”, “utility_bill”, “bank_statement”, “rental_agreement”, “passport_registration”, “temporary_registration”
        :param file_hashes: List of base64-encoded file hashes
        :param message: Error message
        """
        self.source = source
        self.type_ = type_
        self.file_hashes = file_hashes
        self.message = message


class PassportElementErrorUnspecified:
    """Represents an issue in an unspecified place. The error is considered resolved when new data is added."""

    def __init__(self, source: str, type_: str, element_hash: str, message: str):
        """
        :param source: Error source, must be unspecified
        :param type_: Type of element of the user's Telegram Passport which has the issue
        :param element_hash: Base64-encoded element hash
        :param message: Error message
        """
        self.source = source
        self.type_ = type_
        self.element_hash = element_hash
        self.message = message


class Game:
    """This object represents a game. Use BotFather to create and edit games, their short names will act as unique identifiers."""

    def __init__(self, title: str, description: str, photo: List[PhotoSize], text: Optional[str] = None, text_entities: Optional[List[MessageEntity]] = None, animation: Optional[Animation] = None):
        """
        :param title: Title of the game
        :param description: Description of the game
        :param photo: Photo that will be displayed in the game message in chats.
        :param text: Optional. Brief description of the game or high scores included in the game message. Can be automatically edited to include current high scores for the game when the bot calls setGameScore, or manually edited using editMessageText. 0-4096 characters.
        :param text_entities: Optional. Special entities that appear in text, such as usernames, URLs, bot commands, etc.
        :param animation: Optional. Animation that will be displayed in the game message in chats. Upload via BotFather
        """
        self.title = title
        self.description = description
        self.photo = photo
        self.text = text
        self.text_entities = text_entities
        self.animation = animation


class CallbackGame:
    """A placeholder, currently holds no information. Use BotFather to set up your game."""


class GameHighScore:
    """This object represents one row of the high scores table for a game."""

    def __init__(self, position: int, user: User, score: int):
        """
        :param position: Position in high score table for the game
        :param user: User
        :param score: Score
        """
        self.position = position
        self.user = user
        self.score = score


InputFile = Union[InputFile, Tuple[str, IO]]
