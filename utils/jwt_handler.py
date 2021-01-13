






def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    """
        自定义jwt认证成功返回对象
        :param token: token
        :param user: 用户对象
        :param request:
        :return: 用户token,id,户名username,用户头像
        """
    return {
        'token': token,
        'user_id':user.id,
        'username':user.username,
    }
