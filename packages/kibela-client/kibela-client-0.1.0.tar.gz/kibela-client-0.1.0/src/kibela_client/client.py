from typing import Dict, List
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from pydantic import parse_obj_as

from .types import Budget, Connection, User

class KibelaClient:
    def __init__(self, team: str, access_token: str) -> None:
        self.url = f"https://{team}.kibe.la/api/v1"
        self.headers = {"Authorization": f"Bearer {access_token}"}
        transport = AIOHTTPTransport(url=self.url, headers=self.headers)
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    def request(self, request_string: str) -> Dict:
        document = gql(request_string)
        return self.client.execute(document)

    def get_budget(self) -> Budget:
        query = """
        {
            budget {
                consumed
                cost
                remaining
            }
        }
        """
        response = self.request(query)
        return Budget.parse_obj(response["budget"])

    def get_users(self) -> List[User]:
        query = """
        {
            users(first: 10) {
                nodes {
                    account
                    avatarImage {
                        density
                        url
                        height
                        width
                    }
                    biography
                    coverImage {
                        density
                        height
                        key
                        size
                        url
                        width
                    }
                    email
                    id
                    locale
                    path
                    realName
                    role
                    shortBio
                    url
                }
            }
        }
        """
        response = self.request(query)
        user_connection = parse_obj_as(Connection[User], response["users"])
        return user_connection.nodes
