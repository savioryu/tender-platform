<template>
  <div class="app-container">
    <h1 style="text-align: center;">{{ title }}</h1>
    <el-form>
      <el-form-item label-position="top">
        <div ref="editorContent" class="editor-content" v-html="txt" />
      </el-form-item>
      <el-form-item>
        <h1>附件：</h1>
        <div v-for="(attach, index) in attachList" :key="index">
          <el-link type="primary" :href="attach.fileUrl" target="_blank">
            {{ `${attach.fileName}（${attach.fileSize}）` }}
          </el-link>
        </div>
        <div ref="editorContent" class="editor-content" v-html="attachString" />
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getDetail } from '@/api/announcement';
export default {
  filters: {
  },
  data() {
    return {
      attachList: [],
      attachString: '',
      txt: ''
    };
  },
  created() {
    const { contentId } = this.$route.query;
    this.getDetail(contentId);
  },
  methods: {
    getDetail(contentId) {
      getDetail(contentId).then(res => {
        const { data } = res;
        const { title, txt, attachments } = data[0];
        this.title = title;
        this.txt = txt;
        const { attrValue } = attachments;
        try {
          const attachList = JSON.parse(attrValue);
          this.attachList = Object.prototype.toString.call(attachList) === '[object Array]' ? attachList : [attachList];
        } catch (error) {
          this.attachString = attrValue;
        }
      });
    }
  }
};
</script>
