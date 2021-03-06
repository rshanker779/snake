from setuptools import setup, find_namespace_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(name="snake",
      version='1.0.0',
      author="rshanker779",
      author_email="rshanker779@gmail.com",
      description="Python implementation of classic Snake game in pygame",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/rshanker779/snake",
      license='MIT',
      python_requires='>=3.5',
      install_requires=['pygame',
                        'setuptools'],
      packages=['src/game', 'src/game_bots'],
      entry_points={'gui_scripts': ['python-snake=src.game.snake:main',
                                    'random-snake=src.game_bots.random_bot:main',
                                    'distance-snake=src.game_bots.euclidean_distance_bot:main'
                                    ]},

      )
