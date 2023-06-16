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
    <div v-if="img_preview_url">
      <img :src="img_preview_url" id="preview_img">
    </div>
    <button @click="uploadFile">アップロードする</button>
    <button @click="analyze">解析する</button>
  </div>
</template>

<script>
import axios from "axios"
export default {
  name: 'App',
  data() {
    return {
      // 選択した画像ファイル
      img_file_input: "",

      // 画像プレビュー用URL
      img_preview_url: "",

      // 画像アップロードして返ってくるタスクID
      task_id: "",

      // 解析完了のフラグ
      isAnalysisComplete: false,

      // 検出した物体の情報
      detected_objects: {}
    }
  },
  methods: {
    setFile(e) {
      const file = e.target.files[0]
      this.img_file_input = file
      this.img_preview_url = URL.createObjectURL(file)
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
      formData.append("upload_file",this.img_file_input);
      // ヘッダー
      const config = {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }
      // fastAPIを叩く
      try {
        const response = await axios.post("http://localhost:8001/api/analyze", formData, config)
        if (response.status == 200) {
          this.task_id = response.data.id
          console.log(response)
        }
      } catch (e) {
        console.error(e)
      }
    },
    async analyze() {
      // fastAPIを叩く
      try {
        const response = await axios.get("http://localhost:8001/api/analyze/" + this.task_id)
        if (response.status == 200) {
          if (response.data.status == "SUCCESS") {
            this.isAnalysisComplete = true
            this.detected_objects = response.data.result
            console.log(response.data.result)
          } else if (response.data.status == "PENDING") {
            console.log("解析中。。。")
          }
        }
      } catch (e) {
        console.error(e)
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
  margin-top: 60px;
}

#file_input {
  display: none;
}

#preview_img {
  width: 80%;
}
</style>
