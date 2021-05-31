<template>
  <pre><code>{{ data }}</code></pre>
</template>

<script>
export default {
  data() {
    return {
      data: '',
    }
  },
  mounted() {
    this.$axios
      .get('/debug/api/v1/config', {})
      .then(res => {
        if (res.data.status === 0) {
          this.data = JSON.stringify(res.data.data, null, 4)
        } else {
          this.$message.warning(res.data.message)
        }
      })
      .catch(() => {
        this.$message.error('服务异常，请联系管理员姜成龙！')
      })
  },
}
</script>

<style scoped></style>
