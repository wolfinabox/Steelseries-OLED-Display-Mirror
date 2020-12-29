from setuptools import setup, find_packages

requirements = [
    "altgraph==0.17",
    "certifi==2020.6.20",
    "chardet==3.0.4",
    "EasyProcess==0.3",
    "entrypoint2==0.2.1",
    "future==0.18.2",
    "idna==2.10",
    "mss==6.0.0",
    "numpy==1.19.0",
    "pefile==2019.4.18",
    "Pillow==7.2.0",
    "pyinstaller==4.0",
    "pyinstaller-hooks-contrib==2020.7",
    "PySide2==5.15.2",
    "pywin32-ctypes==0.2.0",
    "requests==2.24.0",
    "shiboken2==5.15.2",
    "urllib3==1.25.9",
]

setup(
    author="wolfinabox",
    author_email="jtpetch13@gmail.com>",
    python_requires=">3.5",
    name="steelseries-oled-display-mirror",
    description="Quick hacked together script to \"mirror\" your desktop screen to the "
                "OLED on a SteelSeries device.",
    install_requires=requirements,
    setup_requires=requirements,
    dependency_links=[
        "https://github.com/hbldh/hitherdither/archive/v0.1.5.zip"
    ],
    entry_points={
        "console_scripts": [
            "oled-display-mirror=oled_display_mirror.mainapp:main"
        ]
    },
    packages=find_packages(include=["oled_display_mirror", "oled_display_mirror.*"]),
    version="0.1.0",
    zip_safe=False
)
