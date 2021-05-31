<template>
  <div>
    <a-row type="flex" justify="start" align="middle">
      <a-col :span="3">
        <a-select
          @change="selectById"
          default-value="leads_sn"
          style="width: 120px"
        >
          <a-select-option value="finish_id">问卷号</a-select-option>
          <a-select-option value="user_mobile">手机号</a-select-option>
          <a-select-option value="leads_sn">线索号</a-select-option>
        </a-select>
      </a-col>
      <a-col :span="3">
        <a-input-search
          @search="onSearch"
          placeholder="input search id"
          enter-button
        />
      </a-col>
    </a-row>
    <a-table
      :columns="columns"
      :dataSource="data"
      :pagination="pagination"
      :loading="loading"
      @change="handleTableChange"
      bordered
    >
      <span slot="action" slot-scope="record">
        <a-row>
          <a-col :span="12">
            <div>
              <a-button @click="showLeadsModal(record)" type="danger">
                仅清理线索
              </a-button>
            </div>
          </a-col>
          <a-col :span="12">
            <div>
              <a-button @click="showUserModal(record)" type="danger">
                清理用户和线索
              </a-button>
            </div>
          </a-col>
        </a-row>
      </span>
      <template>
        <a-pagination />
      </template>
    </a-table>
    <a-modal @ok="deleteLeads" v-model="leadsVisible" title="仅清理线索">
      <p>数据删除为物理删除，删除后不可恢复！</p>
      <p>请谨慎进行操作，操作后会对QA环境生效！</p>
      <p>如果您有任何问题请联系管理员刘丽雨！</p>
    </a-modal>
    <a-modal
      @ok="deleteLeadsAndUser"
      v-model="userVisible"
      title="清理用户和线索"
    >
      <p>数据删除为物理删除，删除后不可恢复！</p>
      <p>请谨慎进行操作，操作后会对QA环境生效！</p>
      <p>如果您有任何问题请联系管理员刘丽雨！</p>
    </a-modal>
  </div>
</template>

<script>
const columns = [
  {
    title: '序列号',
    dataIndex: 'id',
    key: 'id',
    width: '8%',
    className: 'column-solid',
  },
  {
    title: '完成标识',
    dataIndex: 'finish_id',
    key: 'finish_id',
    width: '8%',
    className: 'column-solid',
  },
  {
    title: '用户标识',
    dataIndex: 'user_id',
    key: 'user_id',
    width: '8%',
    className: 'column-solid',
  },
  {
    title: '用户姓氏',
    dataIndex: 'last_name',
    key: 'last_name',
    width: '8%',
    className: 'column-solid',
  },
  {
    title: '手机号码',
    dataIndex: 'user_mobile',
    key: 'user_mobile',
    width: '10%',
    className: 'column-solid',
  },
  {
    title: '保险师标识',
    dataIndex: 'admin_user_id',
    key: 'admin_user_id',
    width: '8%',
    className: 'column-solid',
  },
  {
    title: 'FLOW标识',
    dataIndex: 'flow_id',
    key: 'flow_id',
    width: '10%',
    className: 'column-solid',
  },
  {
    title: 'LEADS标识',
    dataIndex: 'leads_sn',
    key: 'leads_sn',
    width: '10%',
    className: 'column-solid',
  },
  {
    title: '操作',
    key: 'action',
    scopedSlots: { customRender: 'action' },
    width: '30%',
    className: 'column-solid',
  },
]

export default {
  data() {
    return {
      data: [],
      leadsVisible: false,
      leadsModel: {},
      userVisible: false,
      userModel: {},
      params: {
        by: 'finish_id',
        id: '',
      },
      pagination: {},
      loading: false,
      columns,
    }
  },
  mounted() {
    this.fetch({ page: 0 })
  },
  methods: {
    handleTableChange(pagination, filters, sorter) {
      console.log('table changed!')
      const pager = { ...this.pagination }
      pager.current = pagination.current
      this.pagination = pager
      this.fetch({
        results: pagination.pageSize,
        page: pagination.current,
        sortField: sorter.field,
        sortOrder: sorter.order,
        ...filters,
        ...this.params,
      })
    },
    showLeadsModal(value) {
      this.leadsVisible = true
      this.leadsModel = value
    },
    showUserModal(value) {
      this.userVisible = true
      this.userModel = value
    },
    selectById(value) {
      console.log(value)
      this.params.by = value
    },
    onSearch(value) {
      console.log(value)
      this.params.id = value
      this.fetch(this.params)
    },
    deleteLeads() {
      console.log(this.leadsModel)
      this.$axios
        .post('/genesis/api/v1/delete', [
          {
            finish_id: this.leadsModel.finish_id,
            leads_sn: this.leadsModel.leads_sn,
            user_id: this.leadsModel.user_id,
            type: 'leads',
          },
        ])
        .then(res => {
          this.fetch()
        })
      this.leadsVisible = false
    },
    deleteLeadsAndUser() {
      console.log(this.userModel)
      this.$axios
        .post('/genesis/api/v1/delete', [
          {
            finish_id: this.userModel.finish_id,
            leads_sn: this.userModel.leads_sn,
            user_id: this.userModel.user_id,
            type: 'user',
          },
        ])
        .then(res => {
          this.fetch()
        })
      this.userVisible = false
    },
    fetch(params = {}) {
      console.log(this.pagination)
      this.loading = true
      this.$axios
        .get('/genesis/api/v1/search', {
          params: {
            size: 10,
            page: this.pagination.current,
            database: 'insurance',
            table: 'ins_questionnaire',
            fields:
              'id,user_id,finish_id,last_name,user_mobile,flow_id,create_time,admin_user_id,leads_sn',
            ...this.params,
          },
        })
        .then(res => {
          console.log(res)
          const pagination = { ...this.pagination }
          pagination.total = res.data.count
          this.loading = false
          this.data = res.data.data
          for (const index in this.data) {
            this.data[index].key = this.data[index].id
          }
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
