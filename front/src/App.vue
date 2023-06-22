<template>
  <v-app>
    <div class="header">
      <header-comp></header-comp>
    </div>
    <v-content class="main">
      <div id="app">
        <img src="./logo.png" width="100%" height="100%">
        <!-- <h2>特定警察とは？？</h2>
        <p>普段皆さんが何気なくuploadする画像に特定で使用されそうな要素が無いかをチェックするためのWebアプリケーションです。</p> -->
        <v-card color="#F2F7FF">
            <v-card-title>
              特定警察とは？？
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text class="text-left">
              皆さんが普段、SNSへアップロードする写真は電柱やマンホールの映り込みによって、特定される危険に晒されています！
              このWebアプリケーションを使って、特定される要素と写真の危険度を把握しましょう！<br>
              <a style="color:gray; font-weight: bold;">このアプリケーションでできること：</a><br>
              ・危険要素を枠で表示(step3)<br>
              ・危険度の表示(step3)<br>
              ・危険要素へモザイクをかけた写真をダウンロード(step4)
            </v-card-text>
        </v-card>
        <br>
        <!-- <h2>使い方</h2>
        <ol>
          <li>ライブラリから画像を選択</li>
          <li>プレビューを確認しアップロード</li>
          <li>画像解析後に結果を確認</li>
        </ol> -->
        <v-card color="#F2F7FF">
            <v-card-title>
              使用手順
            </v-card-title>
            <v-divider></v-divider>
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
        </v-card>
        <br>
        <div class="inputFile">
          <v-btn outlined color="#108CEB" @click="openFile()">画像選択</v-btn>
          <input type="file" id="file_input" accept="image/*, .heic" style="display: none" ref="fileInput" @change="setFile" />
        </div>
        <br>
        <div class="img_container" v-if="imgPreviewUrl">
          <img class="img_prev" :src="imgPreviewUrl" id="preview_img" width="100%" height="100%">
          <svg :width="imgWidth" :height="imgHeight" class="svg_container">
            <rect v-for="(det_object, index) in det_objects" :key="index"
              :x="det_object.x" :y="det_object.y" :width="det_object.w" :height="det_object.h" stroke="red" fill="none" stroke-width="2" />
          </svg>
        </div>
        <br>
        <!-- upload_button -->
        <div class="upload_button" v-if="isVisible">
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
        <h3 v-if="buttonRestricted">↓↓↓文字をぼかした写真をダウンロード↓↓↓</h3>
        <div v-if="canvas">
          <v-btn outlined color="#108CEB" @click="downloadImage">ダウンロード</v-btn>
        </div>
        <img class="download_img">
      </div>
    </v-content>
  </v-app>
</template>


<script>
import axios from "axios"
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
      imgWidth: 10,
      imgHeight: 10,

      //detected_objectsを格納
      //形式例：{'x':100, 'y':100, 'w':200, 'h':100}
      det_objects: [
      ],

      //解析ボタンを画像uploadするまで隠す
      //setFile()でtrueへ
      isVisible : false,

      //解析中のdialogを開閉するタイミングを規定
      dialog:false,

      //使い方の説明手順
      explainItems:[
        "「画像選択」ボタンを押しライブラリから画像を選択",
        "プレビューを確認し「UPLOAD」ボタンを押す",
        "画像解析後に結果(枠・危険度の表示)を確認",
        "「ダウンロード」ボタンを押す"
      ],

      //UPLOADボタンを非表示にするフラグ
      //RESPONSE=200でtrueへ
      buttonRestricted : false
    }
  },
  methods: {
    setFile(e) {
      const file = e.target.files[0]
      this.imgFileInput = file
      this.imgPreviewUrl = URL.createObjectURL(file)
      this.isVisible = true
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
      this.imgWidth = document.getElementById('preview_img').width
      this.imgHeight = document.getElementById('preview_img').height

      formData.append('req', JSON.stringify(req));
      formData.append("upload_file",this.imgFileInput);
      // ヘッダー
      const config = {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }
      try {
        const response = await axios.post("http://localhost:8001/api/analyze", formData, config)
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
      const res = await axios.get("http://localhost:8001/api/analyze/" + this.taskId)
      return res.data
    },

    // ステータスがSUCCESSになるまでAPIを叩く
    async pollAPIAnalyze() {
      const timeId = setInterval(async () => {
        const res = await this.callApiAnalyze()
        if (res.status == "SUCCESS") {
          this.handleSuccessResponse(res)
          clearInterval(timeId)
          this.buttonRestricted=true;
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
    openFile(){
      this.$refs.fileInput.click();
    }
  },
  watch:{
    //det_objectに値が入ればdialogを閉じる
    det_objects(val){
      if(val.length!=0){
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
