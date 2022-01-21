from setuptools import setup, Extension


setup(
    name='nonebot_adapter_mirai2',
    python_requires='>=3.8.0',
    version='0.0.1',
    description='nonebot2.0.0b1 的 mirai_api_http2 适配器',
    author='ieew',
    author_email='i@ieew.cc',
    url='https://github.com/ieew/nonebot2_adapter_mirai',
    packages=['nonebot', 'nonebot.adapters.mirai2', 'nonebot.adapters.mirai2.event'],
    install_requires=['nonebot2>=2.0.0b1'],
    license='GNU AFFERO GENERAL PUBLIC LICENSE',
    keywords=['nonebot2', 'mirai', 'mirai_api_http2']
)
