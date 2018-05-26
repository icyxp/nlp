<template>

      <div>
        <el-upload 
            style="padding-top: 50px"
            class="upload-demo"
            drag
            action="http://api-cnki.innosnap.local/api/upload"
            name="file"
            multiple
            :on-success="successUpload"
            :before-upload="beforeUpload"
            v-loading="fullscreenLoading"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将提案文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">支持上传txt/word/pdf/jpg/png文件，上传成功后进行自动查重</div>
          </el-upload>
          
      </div>
            
</template>

<script>
export default {
  data() {
      return {
        fullscreenLoading: false
      }
  },
  methods: {
    beforeUpload: function(){
      this.fullscreenLoading = true
    },
    successUpload: function(response, file, fileList) {
      this.fullscreenLoading = false
      let uuid = response.result
      let path = '/result/' + uuid
      this.$router.push({ path: path})
    }
  }
}
</script>

<style>
.el-upload-dragger .el-upload__text em {
  color: rgb(100, 177, 5);
}
.el-upload-dragger:hover {
  border: 1px dashed rgb(100, 177, 5);
}
</style>
