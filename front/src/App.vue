<template>
  <div id="app">
    <h1>サービス名</h1>
    <p>
      説明文説明文説明文説明文説明文説明文説明文説明文説明文説明文説明文
      説明文説明文説明文説明文説明文説明文説明文説明文説明文説明文説明文
      説明文説明文説明文説明文説明文説明文説明文説明文説明文説明文説明文
    </p>
    <label for="file_input">
      画像を選択
      <input type="file" id="file_input" accept="image/*, .heic" @change="setFile" />
    </label>
    <div v-if="imgPreviewUrl">
      <img :src="imgPreviewUrl" id="preview_img">
    </div>
    <button @click="uploadFile">解析する</button>
  </div>
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
      detected_objects: {}
    }
  },
  methods: {
    setFile(e) {
      const file = e.target.files[0]
      this.imgFileInput = file
      this.imgPreviewUrl = URL.createObjectURL(file)
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
        } else if (res.status == "PENDING") {
          console.log("PENDINGなので定期的にAPI叩きます")
        }
      },1500);
    },

    handleSuccessResponse(res) {
      this.isAnalysisComplete = true
      this.detected_objects = res.result
      this.applyBlurToDetectedCharacters()
      console.log("解析が完了しました")
    },

    // 検出した文字をぼかす
    applyBlurToDetectedCharacters() {
      const previewImage = document.getElementById('preview_img');
      const canvas = document.createElement('canvas');
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

        context.filter = 'blur(5px)';
        // context.fillStyle = 'black';
        context.fillRect(x, y, 100, 100);
      });

      // 修正した画像を表示するために、修正後のキャンバスをプレビュー画像のsrcに設定する
      previewImage.src = canvas.toDataURL();
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

#preview_img {
  width: 80%;
}
</style>
