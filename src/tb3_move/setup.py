from setuptools import setup

package_name = 'tb3_move'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubumtu',
    maintainer_email='gooda1900@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tb3m = tb3_move.tb3_basic_move:main',
            'tb3s = tb3_move.tb3_sub:main',
            'tb3mix = tb3_move.tb3_mix:main',
            'tb3mix2 = tb3_move.tb3_mix2:main',
            'tb3mix3 = tb3_move.tb3_mix3:main',
            'tb3gpio = tb3_move.gpiotest:main',
            'tb3distance_sub_test = tb3_move.tb3_distance_sub:main',
        ],
    },
)

