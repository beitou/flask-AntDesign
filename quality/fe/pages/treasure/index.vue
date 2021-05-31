<template>
  <div>
    <a-row type="flex" justify="start" align="middle">
      <a-col :span="3">
        <a-select
          @change="handleNameChange"
          default-value="all"
          style="width: 120px"
        >
          <a-select-option value="all">全部</a-select-option>
          <a-select-option value="小帮保险">小帮保险</a-select-option>
          <a-select-option value="小帮规划">小帮规划</a-select-option>
        </a-select>
      </a-col>
      <a-col :span="3">
        <a-select
          @change="handleTypeChange"
          default-value="all"
          style="width: 120px"
        >
          <a-select-option value="all">全部</a-select-option>
          <a-select-option value="debug">Debug</a-select-option>
          <a-select-option value="release">Release</a-select-option>
        </a-select>
      </a-col>
      <a-col :span="3">
        <a-select
          @change="handlePlatformChange"
          default-value="all"
          style="width: 120px"
        >
          <a-select-option value="all">全部</a-select-option>
          <a-select-option value="android">Android</a-select-option>
          <a-select-option value="ios">iOS</a-select-option>
        </a-select>
      </a-col>
      <a-col :span="3">
        <a-button @click="search">搜索</a-button>
      </a-col>
    </a-row>
    <a-table
      :columns="columns"
      :rowKey="record => record.id"
      :dataSource="data"
      :pagination="pagination"
      :loading="loading"
      @change="handleTableChange"
      bordered
    >
      <span slot="action" slot-scope="record">
        <a :href="'/treasure/detail?id=' + record.id">下载</a>
        <a-divider type="vertical" />
        <a
          :href="
            '/treasure/history?name=' +
              record.name +
              '&type=' +
              record.type +
              '&platform=' +
              record.platform
          "
          >历史版本</a
        >
      </span>
    </a-table>
  </div>
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
      params: {
        name: 'all',
        type: 'all',
        platform: 'all',
      },
      pagination: {},
      total: 0,
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
        page: pagination.current,
        sortField: sorter.field,
        sortOrder: sorter.order,
        ...this.params,
      })
    },
    handleNameChange(value) {
      this.params.name = value
    },
    handleTypeChange(value) {
      this.params.type = value
    },
    handlePlatformChange(value) {
      this.params.platform = value
    },
    search() {
      this.pagination.current = 1
      this.fetch()
    },
    fetch(params = {}) {
      console.log('params:', params)
      this.loading = true
      this.$axios
        .get('/treasure/app/search', {
          params: { size: 10, pager: this.pagination.current, ...this.params },
        })
        .then(res => {
          console.log(res)
          const pagination = { ...this.pagination }
          // Read total count from server
          // pagination.total = data.totalCount
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
.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}

th.column-solid,
td.column-solid {
  text-align: right !important;
}
</style>
