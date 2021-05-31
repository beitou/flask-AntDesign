<template>
  <a-table
    :columns="columns"
    :rowKey="record => record.id"
    :dataSource="data"
    :pagination="pagination"
    :loading="loading"
    @change="handleTableChange"
    bordered
  >
    <template slot="title">
      历史版本
    </template>
    <span slot="action" slot-scope="record">
      <a :href="'/treasure/detail?id=' + record.id">下载</a>
    </span>
    <template>
      <a-pagination />
    </template>
  </a-table>
</template>
<script>
const columns = [
  {
    title: '序列号',
    dataIndex: 'id',
    sorter: true,
    width: '8%',
    className: 'column-solid',
  },
  {
    title: '包名',
    dataIndex: 'name',
    sorter: true,
    width: '8%',
    className: 'column-solid',
  },
  {
    title: '版本',
    dataIndex: 'version',
    sorter: true,
    width: '8%',
    className: 'column-solid',
  },
  {
    title: '版本号',
    dataIndex: 'version_name',
    sorter: true,
    width: '8%',
    className: 'column-solid',
  },
  {
    title: '使用环境',
    dataIndex: 'type',
    sorter: true,
    width: '9%',
    className: 'column-solid',
  },
  {
    title: '平台',
    dataIndex: 'platform',
    sorter: true,
    width: '8%',
    className: 'column-solid',
  },
  {
    title: '创建时间',
    dataIndex: 'created',
    sorter: true,
    width: '16%',
    className: 'column-solid',
  },
  {
    title: 'commit_id',
    dataIndex: 'commit_id',
    width: '20%',
    className: 'column-solid',
  },
  {
    title: '操作',
    key: 'action',
    scopedSlots: { customRender: 'action' },
    width: '16%',
    className: 'column-solid',
  },
]

export default {
  data() {
    return {
      data: [],
      pagination: {},
      loading: false,
      columns,
    }
  },
  mounted() {
    this.fetch()
  },
  methods: {
    handleTableChange(pagination, filters, sorter) {
      console.log(pagination)
      const pager = { ...this.pagination }
      pager.current = pagination.current
      this.pagination = pager
      this.fetch({
        results: pagination.pageSize,
        page: pagination.current - 1,
        sortField: sorter.field,
        sortOrder: sorter.order,
        ...filters,
      })
    },
    fetch() {
      console.log(
        this.$route.query.name,
        this.$route.query.type,
        this.$route.query.platform
      )
      this.loading = true
      this.$axios
        .get('/treasure/app/search', {
          params: {
            size: 10,
            pager: this.pagination.current,
            name: this.$route.query.name,
            type: this.$route.query.type,
            platform: this.$route.query.platform,
          },
        })
        .then(res => {
          const pagination = { ...this.pagination }
          pagination.total = res.data.total
          this.loading = false
          this.data = res.data.data
          this.pagination = pagination
        })
    },
  },
}
</script>

<style>
th.column-solid,
td.column-solid {
  text-align: right !important;
}
</style>
