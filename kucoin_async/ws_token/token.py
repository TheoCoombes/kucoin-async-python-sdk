from kucoin_async.base_request.base_request import KucoinBaseRestApi


class GetToken(KucoinBaseRestApi):

    async def get_ws_token(self, is_private=False):
        """
        https://docs.kucoin.com/#apply-connect-token
        :param is_private private or public
        :return:
        """
        uri = '/api/v1/bullet-public'
        if is_private:
            uri = '/api/v1/bullet-private'

        return await self._request('POST', uri, auth=is_private)


