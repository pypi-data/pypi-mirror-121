from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel
from pydantic.generics import GenericModel
from typing import TypeVar, Generic

NodeType = TypeVar("NodeType")


class Edge(GenericModel, Generic[NodeType]):
    node: Optional[NodeType]
    cursor: Optional[str]


class PageInfo(BaseModel):
    start_cursor: Optional[str]
    end_cursor: Optional[str]
    has_next_page: Optional[bool]
    has_previous_page: Optional[bool]


class Connection(GenericModel, Generic[NodeType]):
    nodes: Optional[List[NodeType]]
    edges: Optional[List[Edge[NodeType]]]
    page_info: Optional[PageInfo]
    total_count: Optional[int]


class Budget(BaseModel):
    consumed: Optional[int]
    cost: Optional[int]
    remaining: Optional[int]


class Role(str, Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    FULL_MEMBER = "FULL_MEMBER"
    GUEST = "GUEST"


class UserAvatarImage(BaseModel):
    density: Optional[int]
    height: Optional[int]
    url: Optional[str]
    width: Optional[int]

class UserCoverImageSize(str, Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    ORIGINAL = "ORIGINAL"


class UserCoverImage(BaseModel):
    density: Optional[int]
    height: Optional[int]
    key: Optional[str]
    size: Optional[UserCoverImageSize]
    url: Optional[str]
    width: Optional[int]



class GroupCoverImage(BaseModel):
    density: Optional[int]
    height: Optional[int]
    url: Optional[str]
    width: Optional[int]

class Group(BaseModel):
    archived_at: Optional[datetime]
    can_be_joined: Optional[bool]
    can_be_managed: Optional[bool]
    cover_image: Optional[GroupCoverImage]
    cover_image_key: Optional[str]
    created_at: Optional[datetime]
    description: Optional[str]
    feed_updated_at: Optional[datetime]
    folders: Optional[List["Folder"]]
    id: Optional[str]
    is_archived: Optional[bool]
    is_default: Optional[bool]
    is_joined: Optional[bool]
    is_private: Optional[bool]
    is_visibility_changeable: Optional[bool]
    name: Optional[str]
    notes: Optional[List["Note"]]
    path: Optional[str]
    pinned_notes: Optional[List["Note"]]
    today_contributors: Optional[List["User"]]
    trend_notes: Optional[List["Note"]]
    updated_at: Optional[datetime]
    users: Optional[List["User"]]


class Folder(BaseModel):
    archived_at: Optional[datetime]
    components: Optional[List["Folder"]]
    created_at: Optional[datetime]
    folders: Optional[List["Folder"]]
    full_name: Optional[str]
    group: Optional[Group]
    id: Optional[str]
    last_modified_at: Optional[datetime]
    name: Optional[str]
    new_note_path: Optional[str]
    notes: Optional[List["Note"]]
    parent: Optional["Folder"]
    path: Optional[str]
    pinned_notes: Optional[List["Note"]]
    updated_at: Optional[datetime]


class SearchResult(BaseModel):
    author: Optional["User"]
    content_summary_html: Optional[str]
    content_updated_at: Optional[datetime]
    document: Optional[Union["Comment", "CommentReply", "Note"]]
    path: Optional[str]
    title: Optional[str]
    title_html: Optional[str]
    url: Optional[str]


class ReviewableDraftComment(BaseModel):
    anchor: Optional[str]
    author: Optional["User"]
    content: Optional[str]
    content_html: Optional[str]
    created_at: Optional[datetime]
    id: Optional[str]
    path: Optional[str]


class ReviewableDraft(BaseModel):
    comments: Optional[List[ReviewableDraftComment]]
    id: Optional[str]
    is_enabled: Optional[bool]
    url: Optional[str]

class SharedNote(BaseModel):
    created_at: Optional[datetime]
    id: Optional[str]
    note: Optional["Note"]
    total_pageviews: Optional[int]
    url: Optional[str]


class Note(BaseModel):
    author: Optional["User"]
    can_be_commented: Optional[bool]
    can_be_destroyed: Optional[bool]
    can_be_liked: Optional[bool]
    can_be_updated: Optional[bool]
    coediting: Optional[bool]
    comments: Optional[List["Comment"]]
    comments_count: Optional[int]
    content: Optional[str]
    content_html: Optional[str]
    content_summary_html: Optional[str]
    content_toc_html: Optional[str]
    content_updated_at: Optional[datetime]
    contributors: Optional[List["User"]]
    created_at: Optional[datetime]
    edit_path: Optional[str]
    folders: Optional[List[Folder]]
    groups: Optional[List[Group]]
    id: Optional[str]
    is_archived: Optional[bool]
    is_liked_by_current_user: Optional[bool]
    likers: Optional[List["User"]]
    path: Optional[str]
    published_at: Optional[datetime]
    related_notes: Optional[List[SearchResult]]
    reviewable_draft: Optional[ReviewableDraft]
    selectable_groups: Optional[List[Group]]
    shared_note: Optional[SharedNote]
    title: Optional[str]
    trackback_notes: Optional[List["Note"]]
    updated_at: Optional[datetime]
    url: Optional[str]


class CommentReply(BaseModel):
    anchor: Optional[str]
    author: Optional["User"]
    can_be_liked: Optional[bool]
    can_be_updated: Optional[bool]
    content: Optional[str]
    content_html: Optional[str]
    content_summary_html: Optional[str]
    content_updated_at: Optional[datetime]
    contributors: Optional[List["User"]]
    created_at: Optional[datetime]
    edited_at: Optional[datetime]
    id: Optional[str]
    is_edited: Optional[bool]
    is_liked_by_current_user: Optional[bool]
    likers: Optional[List["User"]]
    path: Optional[str]
    published_at: Optional[datetime]
    updated_at: Optional[datetime]


class Comment(CommentReply):
    replies: Optional[List[CommentReply]]


class User(BaseModel):
    account: Optional[str]
    avatar_image: Optional[UserAvatarImage]
    biography: Optional[str]
    cover_image: Optional[UserCoverImage]
    email: Optional[str]
    groups: Optional[List[Group]]
    id: Optional[str]
    latest_notes: Optional[List["Note"]]
    locale: Optional[str]
    path: Optional[str]
    popular_notes: Optional[List["Note"]]
    private_notes: Optional[List["Note"]]
    real_name: Optional[str]
    role: Optional[Role]
    short_bio: Optional[str]
    url: Optional[str]
