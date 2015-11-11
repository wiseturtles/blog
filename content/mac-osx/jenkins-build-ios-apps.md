Title: Jenkins自动构建iOS应用
Date: 2015-11-11 15:42
Tags: Jenkins, Mac, iOS
Slug: Jenkins-auto-build-iOS-apps
Author: ox0spy
Summary: Jenkins-auto-build-iOS-apps

最近折腾用Jenkins自动构建iOS应用。


## 编译环境

为了构建iOS应用，必须找台Mac电脑做slave。
安装很简单，貌似brew install jenkins就可以了，然后，Jenkins页面上将它加入作为slave。


## 开发者证书

为了可以编译、打包，需要制作开发者证书，并导出为.p12, .cer, .mobileprovision
生成过程自己Google吧。


## 编译、打包命令

同意Xcode和Apple SDK协议:

    :::bash
    $ sudo xcodebuild -license


我用Facebook开源的xctool编译iOS应用，安装xctool。

    :::bash
    $ brew install xctool

我没有使用Jenkins的Xcode插件，直接通过如下命令编译:

    :::bash
    $ xctool -workspace ${WORKSPACE} -scheme ${SCHEME} archive -archivePath "${ARCHIVEPATH}/${IPA_NAME}"
    $ xcrun -sdk iphoneos PackageApplication -v "${PROJECT_BUILDDIR}"/*.app -o "${ARCHIVEPATH}/${IPA_NAME}.ipa"

生成dSYM:

    :::bash
    $ ( cd ${DSYM_INPUT_PATH} ; zip -r -X ${DSYM_ZIP_OUTPUT_PATH} *.dSYM )  # zipping dSYM for testflight upload


## 碰到的问题

### User interaction is not allowed

    :::bash
    $ security unlock-keychain -p <your-passwd> /Users/wlw/Library/Keychains/login.keychain
    $ security show-keychain-info ~/Library/Keychains/login.keychain
    $ set-keychain-settings -t 3600 -l ~/Library/Keychains/login.keychain

开始在命令行运行完还是一直报这个错误，后来，将unlock-keychain命令放在编译命令前就好了。

记得编译前先运行:

    :::bash
    $ security unlock-keychain -p <your-passwd> "$HOME/Library/Keychains/login.keychain"


## 参考文章
- <http://www.egeek.me/2013/02/23/jenkins-and-xcode-user-interaction-is-not-allowed/>
