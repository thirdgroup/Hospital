from captcha.image import ImageCaptcha
from random import randint, shuffle


class GetCaptcha:
    def __init__(self, num):
        self.num = num

    def get_captcha(self, num):
        """
        获取验证码
        :param num: 验证码包含字母和数字分别的个数
        :return: 随机出的验证码在一个字符串中
        """
        result_captcha = []
        for i in range(num):
            letters = randint(65, 90)  # 随机出a-z的一个字母
            figure = randint(48, 57)  # 随机处0-9的一个数字
            result_captcha.append(chr(letters))  # 将字母变成字母
            result_captcha.append(chr(figure))  # 将数字变成数字
        shuffle(result_captcha)  # 将列表随机打乱顺序
        return ''.join(result_captcha)  # 将列表转换成字符串

    def get_captcha_image(self):
        """
        :return:返回验证码的字符串，和验证码的图片对象在一个元组中
        """
        image = ImageCaptcha()
        captcha_str = self.get_captcha(self.num)
        captcha_image = image.generate(captcha_str)
        return captcha_str, captcha_image


if __name__ == '__main__':
    print(GetCaptcha(2).get_captcha_image())
