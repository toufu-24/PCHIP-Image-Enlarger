# 	区分的三次エルミート内挿多項式を用いた画像の高品質化
画像をRGBの3つの要素を持つピクセルの2次元配列とみなし、それぞれに補間アルゴリズムを用いて画像を補間します。

## 結果
PCHIP(区分的三次エルミート内挿多項式)による４倍拡張の結果を以下に示します。
### 農工大の鴨 
|         **Origin**         |   ![元画像](/READMEcomponents/duck/target.png)  |
|:----------------------:|:----------------------:|
|    **Result**   |![補間後](/READMEcomponents/duck/pchip.png)  |


### マンドリル(http://www.ess.ic.kanagawa-it.ac.jp/app_images_j.html より)
|         **Origin**         |   ![元画像](/READMEcomponents/Mandrill/target.png)  |
|:----------------------:|:----------------------:|
|    **Result**   |![補間後](/READMEcomponents/Mandrill/pchip.png)  |

## 実行
Python3.11.3で動作確認をしています。  
pipなどで以下のライブラリをインストールしてください。
```bash
pip install numpy
pip install scipy
pip install openCV-python
```

実行は以下のコマンドで行えます。

``` bash
python pchip.py 画像のPATH 補間倍率 
```
拡大倍率が整数でない場合は、小数点以下を切り捨てた整数倍の拡大倍率に自動的に変換されます。  
pchip_generated.pngという名前で補間後の画像が生成されます。 

### 並列処理
pchip.pyは大きな画像を補間すると時間がかかります。  
そのため、pchip_parallel.pyを用意しました。  
pchip_parallel.pyは複数のプロセスで行うため、pchip.pyよりも高速に補間を行うことができます。  
しかしながら、バグが存在していて、不自然なピクセルが発生することがあるので注意してください。  
実行は以下のコマンドで行えます。

``` bash
python pchip_parallel.py 画像のPATH 補間倍率 
```

## 概要
**scipy.interpolate.PchipInterpolator**を用いて画像のピクセルを補間します。
## 利点
- 高品質化される過程で、不自然なピクセル化が起こらずにきれいな結果になる
- 生成した補間関数を保存しておくことが可能で、その関数から画像を補間することができる

## 欠点
- あくまで補間であるので、とてもきれいになるというわけではない

## 実装
scipy.interpolate.pchip を用いて1次元のPCHIPを縦横に適応することで2次元化しています。  
まず横に適応するために、各行を1次元配列とみなし、PCHIPを適応します。  
次に縦に適応するために、各列を1次元配列とみなし、PCHIPを適応します。  
これにより、2次元配列を補間することができます。  


2倍拡大時を図にすると以下のようになります。  
1を元々の画像のピクセル、2を横に適応した後の画像のピクセル、3を縦に適応した後の画像のピクセルとします。

![補間説明図](/READMEcomponents/pchip_explain.png)

指定された倍率だけピクセル間に挿入することで、画像の補間を実現しています。

## 参考文献
- [scipy.interpolate.PchipInterpolator](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.PchipInterpolator.html)
- [ MATLAB pchip ](https://jp.mathworks.com/help/matlab/ref/pchip.html)

# おまけ
PCHIP以外でも実装を行いました。

### 結果

|         **Origin**         |   ![元画像](/READMEcomponents/duck/target.png)  |
|:----------------------:|:----------------------:|
|    **RectBivariateSpline**   |![2変量スプライン近似](/READMEcomponents/duck/RectBivariateSpline.png)  |
|    **Akima**   |![秋間補間](/READMEcomponents/duck/akima.png)  |
|    **PCHIP**   |![PCHIP](/READMEcomponents/duck/pchip.png)  |

## 矩形メッシュ上の2変量スプライン近似
**scipy.interpolate.RectBivariateSpline**を用いて画像のピクセルを補間します。  
![2変量スプライン近似](/READMEcomponents/duck/RectBivariateSpline.png)

### 利点
- 小数倍率も適用可能
- 関数を保存しておくことができ、その関数から画像を補間することができる
- scipyを用いることで実装が簡単

### 欠点
- 大幅に色が変わる部分で(おそらく)オーバーシュート、アンダーシュートが発生し不自然なピクセルが発生する

### 参考文献
- [scipy.interpolate.RectBivariateSpline](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.RectBivariateSpline.html)

## 秋間補間
**scipy.interpolate.Akima1DInterpolator**を用いて画像のピクセルを補間します。  
![秋間補間](/READMEcomponents/duck/akima.png) 

### 利点
- 2変量スプライン近似よりも不自然なピクセルが少ない

### 欠点
- 大幅に色が変わる部分で(おそらく)オーバーシュート、アンダーシュートが発生し不自然なピクセルが発生する

### 参考文献
- [scipy.interpolate.Akima1DInterpolator](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.Akima1DInterpolator.html)
