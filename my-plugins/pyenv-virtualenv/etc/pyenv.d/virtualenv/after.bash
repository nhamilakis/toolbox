# Actions permormed after creating a virtual-env 

upgrade_packages() {
  PYENV_VERSION=$VIRTUALENV_NAME pyenv-exec pip install --upgrade pip setuptools wheel
}

after_virtualenv 'upgrade_packages'

