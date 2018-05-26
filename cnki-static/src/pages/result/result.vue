<template>
    <div class="demo-block demo-box demo-zh-CN demo-table">
      <el-table
        :data="patents"
        fit
        stripe
        border
        >
        <el-table-column
          prop="patent_name"
          label="提案名称"
          width="200"
          >
        </el-table-column>
        
        <el-table-column
          prop="similar_rate"
          label="相似度"
          width="80"
          >
        </el-table-column>

        <el-table-column
          prop="abstract"
          label="摘要"
          >
        </el-table-column>

      </el-table>
    </el-table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
      data() {
        return {
          patents: []
        }
      },
      created: function () { 
        let uuid = this.$route.params.uuid
        console.log(uuid)
        this.loadData(uuid)
      },
      methods: {
        loadData(uuid){
          let url = 'http://api-cnki.innosnap.local/api/result/' + uuid
          axios.get(url)
          .then((response) => {
            console.log(response);
            this.patents = response.data
          })
          .catch((error) => {
            console.log(error);
          });
        }
      }
    }
</script>

<style>
.demo-block {
    border: 1px solid #ebebeb;
    border-radius: 3px;
    transition: .2s;
}
</style>
