# Maintainer: Jérôme Deuchnord <jerome@deuchnord.fr>

pkgname=kosmorro
pkgver=___VERSION___
pkgrel=1
pkgdesc='A program that computes the ephemerides'

depends=('python>=3.5.0' 'python<4.0.0'
         'python-skyfield>=1.17' 'python-skyfield<2.0.0'
         'python-numpy>=1.17.0' 'python-numpy<2.0.0'
         'python-tabulate')
optdepends=('texlive-bin: PDF creation support'
            'python-latex: PDF creation support')
makedepends=('python-setuptools'
             'ruby-ronn')

arch=('any')
url='http://kosmorro.space'
license=('AGPL3')

source=("https://github.com/Deuchnord/kosmorro/archive/v${pkgver}.tar.gz"
        "locales.tar.xz")
sha256sums=("___HASH_PROGRAM___"
            "___HASH_LOCALES___")

build() {
    pip install --user --isolated Babel
    cp -r ${srcdir}/locales/* ${srcdir}/kosmorro-${pkgver}/kosmorrolib/locales

    cd "${srcdir}/kosmorro-${pkgver}"
    python setup.py build

    cd "${srcdir}/kosmorro-${pkgver}"
    python setup.py compile_catalog build
}

package() {
    cd "${srcdir}/kosmorro-${pkgver}"
    python3 setup.py install --root="${pkgdir}/" --optimize=1 --skip-build
}
