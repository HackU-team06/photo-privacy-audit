<template>
  <v-app>
    <div class="header">
      <header-comp></header-comp>
    </div>
    <v-content class="main">
      <div id="app">
        <h2>使い方</h2>
        <ol>
          <li>ライブラリから画像を選択</li>
          <li>プレビューを確認しアップロード</li>
          <li>画像解析後に結果を確認</li>
        </ol>
        <label for="file_input">
          画像を選択
          <input type="file" id="file_input" accept="image/*, .heic" @change="setFile" />
        </label>
        <!-- 画像変換中のダイアログ -->
        <v-dialog
          v-model="isConverting"
          hide-overlay
          persistent
          width="300"
        >
          <v-card
            color="primary"
            dark
          >
            <v-card-text>
              Please wait...
              <v-progress-linear
                indeterminate
                color="white"
                class="mb-0"
              ></v-progress-linear>
            </v-card-text>
          </v-card>
        </v-dialog>
        <div class="img_container" v-if="imgPreviewUrl">
          <img class="img_prev" :src="imgPreviewUrl" id="preview_img" width="100%" height="100%">
          <svg :width="imgWidth" :height="imgHeight" class="svg_container">
            <rect v-for="(det_object, index) in det_objects" :key="index"
              :x="det_object.x" :y="det_object.y" :width="det_object.w" :height="det_object.h" stroke="red" fill="none" stroke-width="2" />
          </svg>
        </div>
        <br>
        <v-btn v-if="isVisible" @click="uploadFile">解析する</v-btn>
        <div v-if="canvas">
          <button @click="downloadImage">文字をぼかした写真をダウンロード</button>
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
      imgWidth: '0',
      imgHeight: '0',

      //detected_objectsを格納
      //形式例：{'x':100, 'y':100, 'w':200, 'h':100}
      det_objects: [
      ],

      //解析ボタンを画像uploadするまで隠す
      //setFile()でtrueへ
      isVisible : false,
      
      // heif,heicからjpegへの変換中に表示する
      isConverting: false
    }
  },
  methods: {
    async setFile(e) {
      const file = e.target.files[0]

      if (file) {
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
      //upload画像の大きさ格納
      this.imgWidth = document.getElementById('preview_img')?.width || 0
      this.imgHeight = document.getElementById('preview_img')?.height || 0

      formData.append('req', JSON.stringify(req));
      formData.append("upload_file",this.imgFileInput);
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
      const res = await axios.get("/api/analyze/" + this.taskId)
      return res.data
    },

    // ステータスがSUCCESSになるまでAPIを叩く
    async pollAPIAnalyze() {
      const timeId = setInterval(async () => {
        const res = await this.callApiAnalyze()
        if (res.status == "SUCCESS") {
          this.handleSuccessResponse(res)
          clearInterval(timeId)
        } else if (res.status == "PENDING") {
          console.log("PENDINGなので定期的にAPI叩きます")
        }
      },1500);
    },

    handleSuccessResponse(res) {
      console.log('width:' + this.imgWidth + ', height:' + this.imgHeight);
      this.isAnalysisComplete = true
      this.detected_objects = res.result
      this.applyBlurToDetectedCharacters()
      //枠で囲む座標データをdet_objectsにpush
      //形式：{x:100, y:200, w:100, h:100}
      for(var i=0;i < this.detected_objects.length;i++){
        this.det_objects.push({'x':Number(this.detected_objects[i].bounding_box.x), 'y': Number(this.detected_objects[i].bounding_box.y), 'w': Number(this.detected_objects[i].bounding_box.w), 'h': Number(this.detected_objects[i].bounding_box.h)})
        console.log(this.det_objects[0]);
      }
    },

    // 検出した文字をぼかす
    applyBlurToDetectedCharacters() {
      const previewImage = document.getElementById('preview_img');
      const canvas = document.createElement('canvas');
      this.canvas = canvas
      const context = canvas.getContext('2d');

      // 画像の大きさをキャンバスに設定
      canvas.width = previewImage.width;
      canvas.height = previewImage.height;

      // 画像を描画
      context.drawImage(previewImage, 0, 0, canvas.width, canvas.height);

      // 文字の位置情報を元にぼかし処理
      this.detected_objects.forEach(obj => {
        const { x, y, w, h } = obj.bounding_box;
        console.log(x, y, w, h);

        context.filter = 'blur(15px)';
        context.fillRect(x, y, 100, 100);
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
  margin-top: 60px;
}

#file_input {
  display: none;
}


.img-container {
  top:300px;
  left:50px;
}


img{
  left:10px;
}

.download_img{
  display: none;
}

.img_prev{
  position: relative;
}

.svg_container {
  left:10px;
  position: absolute;
}
</style>
