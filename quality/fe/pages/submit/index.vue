<template>
  <div>
    <a-row :gutter="16" justify="start" align="middle">
      <a-col :span="4">
        状态：
        <a-select
          @change="handleStatusChange"
          default-value="全部"
          style="width: 75%"
        >
          <a-select-option value="all">全部</a-select-option>
          <a-select-option value="wait">待测试</a-select-option>
          <a-select-option value="qa">qa测试</a-select-option>
          <a-select-option value="staging">staging测试</a-select-option>
          <a-select-option value="online">已上线</a-select-option>
        </a-select>
      </a-col>
      <a-col :span="4">
        <a-input-search
          @search="onSearch"
          addon_before="搜索："
          placeholder="请输入标题关键字"
          enter-button
        />
      </a-col>
      <a-col :span="3">
        <a-button @click="goSubmitPage" type="primary">提测</a-button>
      </a-col>
    </a-row>
    <a-row>
      <a-table
        :columns="columns"
        :rowKey="record => record.id"
        :dataSource="data"
        :pagination="pagination"
        :loading="loading"
        @change="handleTableChange"
        bordered
      >
        <span slot="status" slot-scope="record">
          <a-tag :color="record.status.color">
            {{ record.status.title }}
          </a-tag>
        </span>
        <span slot="action" slot-scope="record">
          <a-popconfirm
            :visibale="confirm"
            @confirm="confirmStatus(record)"
            title="状态变更后无法撤销"
            ok_text="确认"
            cancel_text="取消"
          >
            <a @click="updateStatus(record)">{{ record.operate.title }}</a>
          </a-popconfirm>
        </span>
        <template>
          <a-pagination />
        </template>
      </a-table>
    </a-row>
  </div>
</template>

<script>
const columns = [
  {
    title: '序列号',
    dataIndex: 'id',
    sorter: true,
    width: '8%',
    align: 'left',
  },
  {
    title: '提测业务',
    dataIndex: 'team',
    sorter: true,
    width: '8%',
    align: 'left',
  },
  {
    title: '提测标题',
    dataIndex: 'name',
    sorter: true,
    width: '16%',
    align: 'left',
  },
  {
    title: '提测人',
    dataIndex: 'submiter_name',
    sorter: true,
    width: '8%',
    align: 'left',
  },
  {
    title: '测试人',
    dataIndex: 'qa_name',
    sorter: true,
    width: '9%',
    align: 'left',
  },
  {
    title: '提测时间',
    dataIndex: 'create_at',
    sorter: true,
    width: '16%',
    align: 'left',
  },
  {
    title: '状态',
    key: 'status',
    scopedSlots: { customRender: 'status' },
    width: '8%',
    align: 'left',
  },
  {
    title: '操作',
    key: 'action',
    scopedSlots: { customRender: 'action' },
    width: '8%',
    align: 'left',
  },
]

export default {
  data() {
    return {
      data: [],
      params: {
        keyword: '',
        submit_status: 'all',
      },
      pagination: {},
      loading: false,
      columns,
      confirm,
    }
  },
  mounted() {
    this.fetch()
  },
  methods: {
    handleTableChange(pagination, filters, sorter) {
      const pager = { ...this.pagination }
      pager.current = pagination.current
      this.pagination = pager
      this.fetch({
        results: pagination.pageSize,
        page: pagination.current - 1,
        sortField: sorter.field,
        sortOrder: sorter.order,
        ...filters,
        ...this.params,
      })
    },
    handleStatusChange(value) {
      this.params.submit_status = value
      this.fetch()
    },
    onSearch(value) {
      this.params.keyword = value
      this.fetch()
    },
    confirmStatus(record) {
      this.$axios
        .get('/submit/api/v1/submit/data/update', {
          params: {
            submit_data_id: record.id,
            operate_status: record.operate.value,
          },
        })
        .then(res => {
          if (res.data.status === 0) {
            this.fetch()
          } else {
            this.$message.error(res.data.message)
          }
        })
        .catch(() => {
          this.$message.error('服务异常，请联系管理员姜成龙！')
        })
    },
    updateStatus(record) {
      // 这里做个区分，如果是查看则跳测试报告页面，否则请求接口更新页面。
      if (record.operate.title === '查看') {
        this.$router.push({
          path: '/submit/report',
          query: {
            id: record.id,
          },
        })
      } else {
        this.confirm = true
      }
    },
    fetch() {
      this.loading = true
      this.$axios
        .get('/submit/api/v1/submit/data/search', {
          params: { size: 10, ...this.params },
        })
        .then(res => {
          const pagination = { ...this.pagination }
          pagination.total = res.data.total
          this.loading = false
          this.data = res.data.data
          for (var i = 0; i < this.data.length; i++) {
            var status = this.data[i].submit_status
            if (status === 'wait') {
              this.data[i].status = {
                title: '待测试',
                color: 'pink',
              }
              this.data[i].operate = {
                title: 'qa测试',
                value: 'qa',
                type: 'primary',
              }
            }
            if (status === 'qa') {
              this.data[i].status = {
                title: 'qa测试',
                color: 'green',
              }
              this.data[i].operate = {
                title: 'staging测试',
                value: 'staging',
                type: 'default',
              }
            }
            if (status === 'staging') {
              this.data[i].status = {
                title: 'staging测试',
                color: 'blue',
              }
              this.data[i].operate = {
                title: '上线',
                value: 'online',
                type: 'danger',
              }
            }
            if (status === 'online') {
              this.data[i].status = {
                title: '已上线',
                color: 'purple',
              }
              this.data[i].operate = {
                title: '查看',
                value: 'finish',
                type: 'dashed',
              }
            }
            if (status === 'finish') {
              this.data[i].status = {
                title: '已完成',
                color: 'purple',
              }
              this.data[i].operate = {
                title: '查看',
                value: 'finish',
                type: 'dashed',
              }
            }
          }
          this.pagination = pagination
        })
        .catch(() => {
          this.$message.error('服务异常，请联系管理员姜成龙！')
        })
    },
    goSubmitPage() {
      this.$router.push({ path: '/submit/submit' })
    },
  },
}
</script>

<style lang="less" scoped>
.ant-row {
  padding-top: 20px;
  padding-bottom: 20px;
}

th.column-solid,
td.column-solid {
  text-align: right !important;
}

.custom {
  border: 1px solid purple;
  border-radius: 4px;
  cursor: pointer;
  opacity: 1;
  color: purple;
  backgroud-color: fff;
  transition: all 0.3s cubic-bezier(0.215, 0.61, 0.355, 1);
}
</style>
