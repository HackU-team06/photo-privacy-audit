<template>
  <v-app>
    <div class="header">
      <header-comp></header-comp>
    </div>
    <v-content class="main">
      <div id="app">
        <!-- アプリのロゴ -->
        <img src="./logo.png" width="100%" height="100%">
        <!-- アプリの説明文 -->
        <v-card color="#F2F7FF">
          <v-card-title>
            特定警察とは？？
            <v-spacer></v-spacer>
            <v-btn rounded class="fab" color="#F2F7FF" @click="show = !show">
              <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
            </v-btn>
          </v-card-title>
          <v-divider></v-divider>
          <v-expand-transition>
            <div v-show="show">
              <v-card-text class="text-left">
              皆さんが普段、SNSへアップロードする写真は電柱やマンホールの映り込みによって、特定される危険に晒されています！
              このWebアプリケーションを使って、特定される要素と写真の危険度を把握しましょう！<br>
              <a style="color:gray; font-weight: bold;">このアプリケーションでできること：</a><br>
              ・危険要素を枠で表示(step3)<br>
              ・危険度の表示(step3)<br>
                    (危険度0:黄，危険度1:オレンジ，危険度2:赤)<br>
              ・危険要素へモザイクをかけた写真をダウンロード(step4)
              </v-card-text>
            </div>
          </v-expand-transition>
        </v-card>
        <br>
        <!-- 使用手順の説明文 -->
        <v-card color="#F2F7FF">
            <v-card-title>
              使用手順
              <v-spacer></v-spacer>
              <v-btn rounded class="fab" color="#F2F7FF" @click="show2 = !show2">
                <v-icon>{{ show2 ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </v-card-title>
            <v-divider></v-divider>
            <v-expand-transition>
              <div v-show="show2">
                <v-card-text>
                  <v-list color="#F2F7FF">
                    <v-list-item v-for="(item, index) in explainItems" :key="index">
                      <v-list-item-content>
                        <v-list-item-title class="text-left">step{{ index + 1 }}</v-list-item-title>
                        <v-list-item-subtitle class="text-left">{{ item }}</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </div>
            </v-expand-transition>
        </v-card>
        <br>
        <!-- explain -->
        <v-card color="#F2F7FF">
          <v-card-title>
            検出したモノの一覧
            <v-spacer></v-spacer>
            <v-btn rounded class="fab" color="#F2F7FF" @click="show3 = !show3">
              <v-icon>{{ show3 ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
            </v-btn>
          </v-card-title>
          <v-divider></v-divider>
          <v-expand-transition>
            <div v-show="show3">
              <v-card-text class="text-left">
              解析後に結果を表示
              </v-card-text>
            </div>
          </v-expand-transition>
        </v-card>
        <br>
        <!-- 画像のインプット -->
        <div class="inputFile">
          <v-btn outlined color="#108CEB" @click="openFile()">画像選択</v-btn>
          <input  type="file"
                  id="file_input"
                  accept="image/png,
                          image/jpeg,
                          image/bmp,
                          image/webp,
                          image/gif,
                          image/heif,
                          image/heic,
                          .heif,
                          .heic"
                  style="display: none"
                  ref="fileInput"
                  @change="setFile"
          />
        </div>
        <br>
        <!-- 画像変換中のダイアログ -->
        <v-dialog
          v-model="isConverting"
          hide-overlay
          persistent
          width="300"
        >
          <v-card color="white" outlined>
            <v-card-text>
              Please wait...
              <v-progress-linear
                indeterminate
                color="#108CEB"
                class="mb-0"
              ></v-progress-linear>
            </v-card-text>
          </v-card>
        </v-dialog>
        <!-- プレビューの表示&svgの描画 -->
        <div class="img_container" v-if="imgWidth > 0 && imgHeight > 0">
          <svg id="svg_container" :viewBox="`0 0 ${imgWidth} ${imgHeight}`" class="svg_container" xmlns:xlink="http://www.w3.org/1999/xlink">
            <image v-if="imgPreviewUrl" :href="imgPreviewUrl" x="0" y="0" :width="imgWidth" :height="imgHeight"
              preserveAspectRatio="none" />
            <rect v-for="(det_object, index) in det_objects" :key="index" :x="det_object.x" :y="det_object.y"
              :width="det_object.w" :height="det_object.h" :stroke="selectColor(det_object.rate)" fill="none" :stroke-width="1 / imgViewScale" />
          </svg>
        </div>
        <br>
        <!-- upload_button -->
        <div class="upload_button" style="text-align: center;" v-if="isVisible">
          <v-btn
              :disabled="buttonRestricted"
              :loading="dialog"
              color="#108CEB"
              outlined
              @click="dialog = true; uploadFile();"
          > Upload </v-btn>
          <v-dialog
              v-model="dialog"
              :scrim="false"
              persistent
              width="auto"
          >
              <v-card color="white" outlined>
                  <v-card-text>
                      analyzing...(Please wait!)
                      <v-progress-linear
                          indeterminate
                          color="#108CEB"
                      ></v-progress-linear>
                  </v-card-text>
              </v-card>
          </v-dialog>
        </div>
        <h3 v-if="buttonRestricted">↓↓↓文字を隠した写真をダウンロード↓↓↓</h3>
        <!-- ダウンロードボタン -->
        <div v-if="canvas">
          <v-btn outlined color="#108CEB" @click="downloadImage">Download</v-btn>
        </div>
        <img class="download_img">
      </div>
    </v-content>
  </v-app>
</template>


<script>
import axios from "axios"
import heic2any from "heic2any";
export default {
  name: 'App',
  data() {
    return {
      // 選択した画像ファイル
      imgFileInput: "",

      // 画像プレビュー用URL
      imgPreviewUrl: "",

      // 画像アップロードして返ってくるタスクID
      taskId: "",

      // 解析完了のフラグ
      isAnalysisComplete: false,

      // 検出した物体の情報
      detected_objects: {},

      canvas: "",

      //uploadされる画像の大きさ情報
      //画像がuploadされれば大きさを更新
      imgWidth: 0,
      imgHeight: 0,

      // SVGの `表示上の大きさ / 内容の大きさ` の比率
      imgViewScale: 1,

      //detected_objectsを格納
      //形式例：{'x':100, 'y':100, 'w':200, 'h':100}
      det_objects: [
      ],

      //解析ボタンを画像uploadするまで隠す
      //setFile()でtrueへ
      isVisible: false,

      //解析中のdialogを開閉するタイミングを規定
      dialog: false,

      //使い方の説明手順
      explainItems: [
        "「画像選択」ボタンを押しライブラリから画像を選択",
        "プレビューを確認し「UPLOAD」ボタンを押す",
        "画像解析後に結果(枠・危険度の表示)を確認",
        "「DOWNLOAD」ボタンを押す"
      ],

      //UPLOADボタンを非表示にするフラグ
      //RESPONSE=200でtrueへ
      buttonRestricted: false,

      //アプリの説明用
      show: false,

      //使用手順の説明用
      show2: false,

      show3: false,

      // heif,heicからjpegへの変換中に表示する
      isConverting: false,

      // 画像バッファ (imgの代わり)
      imgBuffer: null
    }
  },
  methods: {
    async setFile(e) {
      const file = e.target.files[0]
      if (file) {
        // 既存のObjectURLを解放する
        URL.revokeObjectURL(this.imgPreviewUrl);

        if (file.type === 'image/heif' ||
          file.type === 'image/heic' ||
          file.name.toLowerCase().endsWith('.heif') ||
          file.name.toLowerCase().endsWith('.heic')) {
          // heif,heicの場合プレビュー表示できないのでpngに変換する
          // 変換に時間がかかるのでモーダルを表示
          this.isConverting = true
          const convertedImage = await heic2any({
            blob: file,
            toType: 'image/png'
          });
          this.imgFileInput = convertedImage;
          this.imgPreviewUrl = URL.createObjectURL(convertedImage);
          this.isConverting = false
        } else {
          this.imgFileInput = file
          this.imgPreviewUrl = URL.createObjectURL(file)
        }

        console.log(this.imgPreviewUrl);

        // 画像のwidth, heightを取得
        this.imgBuffer = await new Promise((resolve, reject) => {
          const image = new Image();
          image.onload = () => {
            resolve(image);
          };
          image.onerror = () => {
            reject("画像の読み込みに失敗しました");
          };
          image.src = this.imgPreviewUrl;
        });
        this.imgWidth = this.imgBuffer.naturalWidth;
        this.imgHeight = this.imgBuffer.naturalHeight;
        this.buttonRestricted = false;

        // 解析ボタンを表示
        this.isVisible = true

        // 一度解析して別画像を選択したときを考慮して、canvasを初期化
        this.canvas = ""
      }
    },
    async uploadFile() {
      let formData = new FormData()
      // オプション
      const req = {
        config: {
          foo: true,
          bar: 0,
          baz: "string"
        }
      }

      formData.append('req', JSON.stringify(req));
      formData.append("upload_file", this.imgFileInput);
      // ヘッダー
      const config = {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }
      try {
        const response = await axios.post("/api/analyze", formData, config)
        if (response.status == 200) {
          this.taskId = response.data.id
          console.log(response)
          // 画像を解析する
          this.analyze()
        }
      } catch (e) {
        console.error(e)
      }
    },
    async analyze() {
      const res = await this.callApiAnalyze()
      if (res.status == "PENDING") {
        console.log("PENDINGなので定期的にAPI叩きます")
        await this.pollAPIAnalyze()
      } else if (res.status == "SUCCESS") {
        this.handleSuccessResponse(res)
      } else {
        console.log("APIエラーが発生しました")
      }
    },
    async callApiAnalyze() {
      try {
        const res = await axios.get("/api/analyze/" + this.taskId)
        return res.data
      } catch (e) {
        alert("エラーが発生しました。ページをリロードします。")
        location.reload()
      }
    },

    // ステータスがSUCCESSになるまでAPIを叩く
    async pollAPIAnalyze() {
      const timeId = setInterval(async () => {
        try {
          const res = await this.callApiAnalyze()
          if (res.status == "SUCCESS") {
            this.handleSuccessResponse(res)
            clearInterval(timeId)
            this.buttonRestricted = true;
          } else if (res.status == "PENDING") {
            console.log("PENDINGなので定期的にAPI叩きます")
          }
        } catch (e) {
          clearInterval(timeId)
        }
      }, 1500);
    },

    handleSuccessResponse(res) {
      console.log('width:' + this.imgWidth + ', height:' + this.imgHeight);
      const svgWidth = document.querySelector('#svg_container')?.clientWidth ?? 0;
      this.imgViewScale = svgWidth / this.imgWidth;
      console.log('svgWidth:' + svgWidth + ', imgViewScale:' + this.imgViewScale);
      this.isAnalysisComplete = true;
      this.detected_objects = res.result;
      this.applyBlackPaintToDetectedCharacters()
      //枠で囲む座標データをdet_objectsにpush
      //形式：{x:100, y:200, w:100, h:100}
      for (var i = 0; i < this.detected_objects.length; i++) {
        this.det_objects.push({ 'x': Number(this.detected_objects[i].bounding_box.x), 'y': Number(this.detected_objects[i].bounding_box.y),
                                'w': Number(this.detected_objects[i].bounding_box.w), 'h': Number(this.detected_objects[i].bounding_box.h), 
                                'name':this.detected_objects[i].name, 'rate': this.detected_objects[i].rate});
        // console.log(this.det_objects[i]);
        // console.log(this.selectColor(this.det_objects[i].rate));
      }
    },

    // 検出した文字を黒塗りにする
    applyBlackPaintToDetectedCharacters() {
      const previewImage = this.imgBuffer;
      const canvas = document.createElement('canvas');
      this.canvas = canvas
      const context = canvas.getContext('2d');

      // 画像の大きさをキャンバスに設定
      canvas.width = previewImage.naturalWidth;
      canvas.height = previewImage.naturalHeight;

      // 画像を描画
      context.drawImage(previewImage, 0, 0, canvas.width, canvas.height);

      // 文字の位置情報を元に黒塗り
      this.detected_objects.forEach(obj => {
        if (obj.name =="letter") {
          const { x, y, w, h } = obj.bounding_box;
          console.log(x, y, w, h);
          context.fillRect(x, y, w, h);
        }
      });
    },
    downloadImage() {
      const canvas = this.canvas;
      const link = document.createElement('a');

      // 画像のダウンロード用リンクを作成
      link.href = canvas.toDataURL();
      link.download = 'canvas_image.png';

      // リンクをクリックしてダウンロードを開始
      link.click();
    },
    openFile() {
      this.$refs.fileInput.click();
    },
    selectColor(rate){
      if(rate == 2) return 'red'
      else if(rate == 1) return 'orange'
      else return 'yellow'
    }
  },
  watch: {
    //det_objectに値が入ればdialogを閉じる
    det_objects(val) {
      if (val.length != 0) {
        this.dialog = false;
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 40px;
}

#file_input {
  display: none;
}


.img-container {
  top: 300px;
  left: 50px;
}


/* img{
  left:10px;
} */

.download_img {
  display: none;
}


.img_container {
  position: relative;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
}

</style>
