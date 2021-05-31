<template>
  <div>
    <div class="bg-white">
      <a-form
        :form="form"
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 18 }"
        layout="horizontal"
      >
        <h2 class="text-center text-2xl leading-loose">项目信息</h2>
        <a-form-item label="项目名称">
          <a-input
            v-decorator="[
              '项目名称',
              {
                rules: [
                  {
                    required: true,
                    whitespace: true,
                    message: '项目名称必填哦!',
                  },
                ],
              },
            ]"
          />
        </a-form-item>
        <a-form-item label="版本号">
          <a-input
            v-model="submit.project.version"
            placeholder="例如2.1.0，没有版本号不需要填写。"
          ></a-input>
        </a-form-item>
        <a-row>
          <a-col :span="12">
            <a-form-item
              :label-col="{ span: 8 }"
              :wrapper-col="{ span: 15 }"
              label="产品经理"
            >
              <a-select
                @change="selectedPM"
                :filterOption="filterOption"
                v-decorator="[
                  '产品经理',
                  {
                    rules: [
                      {
                        type: 'array',
                        required: true,
                        whitespace: true,
                        message: '至少选择一位产品哦!',
                      },
                    ],
                  },
                ]"
                option-filter-prop="children"
                mode="tags"
                placeholder="请选择产品"
                style="width: 100%"
              >
                <a-select-option
                  v-bind:value="user.userid"
                  v-for="user in role.pm"
                  v-bind:key="user.userid"
                >
                  {{ user.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item
              :label-col="{ span: 4 }"
              :wrapper-col="{ span: 16 }"
              label="测试人员"
            >
              <a-select
                @change="selectedQA"
                :filterOption="filterOption"
                v-decorator="[
                  '测试人员',
                  {
                    rules: [
                      {
                        type: 'array',
                        required: true,
                        whitespace: true,
                        message: '至少选择一位测试哦!',
                      },
                    ],
                  },
                ]"
                option-filter-prop="children"
                mode="tags"
                placeholder="请选择测试"
                style="width: 100%"
              >
                <a-select-option
                  v-bind:value="user.userid"
                  v-for="user in role.qa"
                  v-bind:key="user.userid"
                >
                  {{ user.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-row>
          <a-col :span="12">
            <a-form-item
              :label-col="{ span: 8 }"
              :wrapper-col="{ span: 15 }"
              label="前端开发"
            >
              <a-select
                @change="selectedFE"
                v-model="submit.project.fe"
                :filterOption="filterOption"
                option-filter-prop="children"
                mode="tags"
                placeholder="请选择前端"
                style="width: 100%"
              >
                <a-select-option
                  v-bind:value="user.userid"
                  v-for="user in role.fe"
                  v-bind:key="user.userid"
                >
                  {{ user.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item
              :label-col="{ span: 4 }"
              :wrapper-col="{ span: 16 }"
              label="后端开发"
            >
              <a-select
                @change="selectedRD"
                v-model="submit.project.rd"
                :filterOption="filterOption"
                option-filter-prop="children"
                mode="tags"
                placeholder="请选择后端"
                style="width: 100%"
              >
                <a-select-option
                  v-bind:value="user.userid"
                  v-for="user in role.rd"
                  v-bind:key="user.userid"
                >
                  {{ user.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item label="需求文档">
          <a-input
            v-model="submit.project.prd"
            placeholder="例如FNDN-898或http://jira.xiaobangtouzi.com/browse/FNDN-898"
          ></a-input>
        </a-form-item>
        <a-form-item label="技术文档">
          <a-input v-model="submit.project.tech"></a-input>
        </a-form-item>
        <h2 class="text-center text-2xl leading-loose">环境信息</h2>
        <a-row>
          <a-col :span="8">
            <a-form-item
              :label-col="{ span: 12 }"
              :wrapper-col="{ span: 12 }"
              label="提测业务"
            >
              <a-select
                @change="selectTeam"
                v-decorator="[
                  '提测业务',
                  {
                    rules: [
                      {
                        required: true,
                        whitespace: true,
                        message: '请选择提测业务!',
                      },
                    ],
                  },
                ]"
              >
                <a-select-option value="3">基础服务</a-select-option>
                <a-select-option value="4">保险服务</a-select-option>
                <a-select-option value="5">财商基金</a-select-option>
                <a-select-option value="6">保险供应链</a-select-option>
                <a-select-option value="7">数据平台</a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item
              :label-col="{ span: 8 }"
              :wrapper-col="{ span: 12 }"
              label="Sprint"
            >
              <a-select
                @change="selectSprint"
                v-model="submit.environment.jira.sprint"
              >
                <a-select-option
                  :value="item.id"
                  v-for="item in sprints"
                  :key="item.id"
                >
                  {{ item.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item
              :label-col="{ span: 6 }"
              :wrapper-col="{ span: 12 }"
              label="需求卡片"
            >
              <a-select v-model="submit.environment.jira.card">
                <a-select-option
                  :value="item.key"
                  v-for="item in demands"
                  :key="item.key"
                >
                  {{ item.key }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-row>
          <a-col :span="8">
            <a-form-item
              :label-col="{ span: 12 }"
              :wrapper-col="{ span: 12 }"
              label="代码group"
            >
              <a-select
                @change="selectGroup"
                v-model="submit.environment.git.group"
              >
                <a-select-option value="backend">
                  backend
                </a-select-option>
                <a-select-option value="infra">
                  infra
                </a-select-option>
                <a-select-option value="fq">
                  fq
                </a-select-option>
                <a-select-option value="insurance">
                  insurance
                </a-select-option>
                <a-select-option value="common">
                  common
                </a-select-option>
                <a-select-option value="data">
                  data
                </a-select-option>
                <a-select-option value="apps">
                  apps
                </a-select-option>
                <a-select-option value="frontend">
                  frontend
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item
              :label-col="{ span: 8 }"
              :wrapper-col="{ span: 12 }"
              label="代码库repository"
            >
              <a-select
                @change="selectBranch"
                v-model="submit.environment.git.repository"
              >
                <a-select-option
                  :value="item.id"
                  v-for="item in repos"
                  :key="item.id"
                >
                  {{ item.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
          <a-col :span="8">
            <a-form-item
              :label-col="{ span: 6 }"
              :wrapper-col="{ span: 12 }"
              label="代码库branch"
            >
              <a-select
                @change="selectBranch"
                v-model="submit.environment.git.branch"
              >
                <a-select-option
                  :value="item.id"
                  v-for="item in branchs"
                  :key="item.id"
                >
                  {{ item.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>
        <a-form-item :wrapper-col="{ span: 18 }" label="测试地址">
          <a-input
            v-decorator="[
              '测试地址',
              {
                rules: [
                  {
                    required: true,
                    whitespace: true,
                    message: '请填写测试地址!',
                  },
                ],
              },
            ]"
            placeholder="请填本次修改回归的测试地址"
          />
        </a-form-item>
        <h2 class="text-center text-2xl leading-loose">提测准入</h2>
        <a-row>
          <a-col :span="12">
            <a-form-item
              :label-col="{ span: 8 }"
              :wrapper-col="{ span: 16 }"
              label="是否自测"
            >
              <a-radio-group v-model="submit.admittance.selftest">
                <a-radio :value="true">是</a-radio>
                <a-radio :value="false">否</a-radio>
              </a-radio-group>
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item
              :label-col="{ span: 4 }"
              :wrapper-col="{ span: 18 }"
              label="冒烟用例"
            >
              <a-switch
                v-model="submit.admittance.smoke"
                checked-children="执行通过"
                un-checked-children="执行没过"
              ></a-switch>
            </a-form-item>
          </a-col>
        </a-row>
        <a-row>
          <a-col :span="12">
            <a-form-item
              :label-col="{ span: 8 }"
              :wrapper-col="{ span: 16 }"
              label="前端耗时"
            >
              <a-range-picker
                @change="fillFEDevelopTime"
                v-decorator="[
                  '前端耗时',
                  {
                    rules: [
                      {
                        type: 'array',
                        required: true,
                        whitespace: true,
                        message: '请填写前端耗时!',
                      },
                    ],
                  },
                ]"
              />
            </a-form-item>
          </a-col>
          <a-col :span="12">
            <a-form-item
              :label-col="{ span: 4 }"
              :wrapper-col="{ span: 18 }"
              label="后端耗时"
            >
              <a-range-picker
                @change="fillRDDevelopTime"
                v-decorator="[
                  '后端耗时',
                  {
                    rules: [
                      {
                        type: 'array',
                        required: true,
                        whitespace: true,
                        message: '请填写后端耗时!',
                      },
                    ],
                  },
                ]"
              />
            </a-form-item>
          </a-col>
        </a-row>
        <a-row>
          <a-form-item :wrapper-col="{ span: 18 }" label="影响面">
            <a-textarea
              v-model="submit.admittance.influence"
              :autosize="{ minRows: 6 }"
              placeholder="请填本次修改可能的影响"
            >
            </a-textarea>
          </a-form-item>
        </a-row>
        <a-row>
          <a-form-item
            :label-col="{ span: 4 }"
            :wrapper-col="{ span: 18 }"
            label="自测点"
          >
            <a-textarea
              v-model="submit.admittance.testcase"
              :autosize="{ minRows: 6 }"
              placeholder="请填写自测点"
            >
            </a-textarea>
          </a-form-item>
        </a-row>
      </a-form>
      <a-row>
        <a-col :span="20">
          <a-form-item
            :label-col="{ span: 5 }"
            :wrapper-col="{ span: 18 }"
            label="抄送"
          >
            <a-input v-model="submit.cc_recs" />
          </a-form-item>
        </a-col>
        <a-col :span="2">
          <a-button @click="submitToQA" type="primary" class="">提交</a-button>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      role: {},
      sprints: [],
      demands: [],
      repos: [],
      branchs: [],
      submit: {
        submiter: '',
        cost: {
          fe: {
            start: '',
            end: '',
          },
          rd: {
            start: '',
            end: '',
          },
        },
        cc_recs: 'developer@xiaobangtouzi.com,pdc@xiaobangtouzi.com',
        project: {
          name: '',
          version: '',
          prd: '',
          tech: '',
        },
        environment: {
          jira: {
            team: '3',
            sprint: '',
            card: '',
          },
          git: {
            group: '',
            repository: '',
            branch: '',
          },
          host: '',
        },
        admittance: {
          selftest: true,
          testcase: '',
          smoke: true,
          influence: '',
        },
      },
      form: this.$form.createForm(this),
    }
  },
  mounted() {
    this.initUser()
    this.initSprint()
  },
  methods: {
    initUser() {
      this.$axios.get('/user/role/', {}).then(res => {
        if (res.data.status === 0) {
          this.role = res.data.data
        } else {
          this.$notification.error({
            message: '初始化错误',
            description: '错误' + res.data.status + '：' + res.data.message,
          })
        }
      })
    },
    initSprint() {
      this.$axios
        .get('/submit/api/v1/search/sprint', {
          params: { team: this.submit.environment.jira.team },
        })
        .then(res => {
          if (res.data.status === 0) {
            this.sprints = res.data.data
          } else {
            this.$notification.error({
              message: '初始化错误',
              description: '错误' + res.data.status + '：' + res.data.message,
            })
          }
        })
    },
    initRepo() {
      this.$axios
        .get('/submit/api/v1/search/repository', {
          params: {
            group: this.submit.environment.git.group,
          },
        })
        .then(res => {
          if (res.data.status === 0) {
            this.repos = res.data.data
          } else {
            this.$notification.error({
              message: '初始化错误',
              description: '错误' + res.data.status + '：' + res.data.message,
            })
          }
        })
    },
    selectedPM(value) {
      this.submit.project.pm = value
    },
    selectedQA(value) {
      this.submit.project.qa = value
    },
    selectedFE(value) {
      this.submit.project.fe = value
    },
    selectedRD(value) {
      this.submit.project.rd = value
    },
    filterOption(input, option) {
      // eslint-disable-next-line
      return option.componentOptions.children[0].text.indexOf(input) >= 0
    },
    selectTeam(value) {
      this.initSprint()
    },
    selectSprint(value) {
      this.submit.environment.jira.sprint = value
      this.$axios
        .get('/submit/api/v1/search/demand', {
          params: { sprint: value },
        })
        .then(res => {
          if (res.data.status === 0) {
            this.demands = res.data.data
          } else {
            this.$notification.error({
              message: '初始化错误',
              description: '错误' + res.data.status + '：' + res.data.message,
            })
          }
        })
    },
    selectGroup(value) {
      this.submit.environment.git.group = value
      this.initRepo()
    },
    selectBranch() {
      this.$axios
        .get('/submit/api/v1/search/branch', {
          params: {
            repository: this.submit.environment.git.repository,
          },
        })
        .then(res => {
          if (res.data.status === 0) {
            this.branchs = res.data.data
          } else {
            this.$notification.error({
              message: '初始化错误',
              description: '错误' + res.data.status + '：' + res.data.message,
            })
          }
        })
    },
    fillFEDevelopTime(date, dateString) {
      this.submit.cost.fe.start = dateString[0]
      this.submit.cost.fe.end = dateString[1]
    },
    fillRDDevelopTime(date, dateString) {
      this.submit.cost.rd.start = dateString[0]
      this.submit.cost.rd.end = dateString[1]
    },
    submitToQA(e) {
      /*
       * 预处理请求数据，因为这里不知道更好的处理办法，目前只能这样做。
       * 不要问我为啥，有bug呗，能解决我会复制这么大一坨屎一样的数据？
       */
      let parameter = {
        submiter: {
          姜成龙: 'jiangchenglong@xiaobangtouzi.com',
        },
        cost: this.submit.cost,
        cc_recs: this.submit.cc_recs,
        environment: this.submit.environment,
        admittance: this.submit.admittance,
        project: {
          name: this.form.getFieldValue('项目名称'),
          version: this.submit.project.version,
          pm: {},
          fe: {},
          rd: {},
          qa: {},
          prd: this.submit.project.prd,
          tech: this.submit.project.tech,
        },
      }
      parameter.environment.host = this.form.getFieldValue('测试地址')
      // 处理pm数据
      const pms = this.submit.project.pm
      for (const id in pms) {
        for (const u in this.role.pm) {
          if (pms[id] === this.role.pm[u].userid) {
            const name = this.role.pm[u].name
            const email = this.role.pm[u].email
            parameter.project.pm[name] = email
          }
        }
      }
      // 处理qa数据
      const qas = this.submit.project.qa
      for (const id in qas) {
        for (const u in this.role.qa) {
          if (qas[id] === this.role.qa[u].userid) {
            const name = this.role.qa[u].name
            const email = this.role.qa[u].email
            parameter.project.qa[name] = email
          }
        }
      }
      // 处理fe数据
      const fes = this.submit.project.fe
      for (const id in fes) {
        for (const u in this.role.fe) {
          if (fes[id] === this.role.fe[u].userid) {
            const name = this.role.fe[u].name
            const email = this.role.fe[u].email
            parameter.project.fe[name] = email
          }
        }
      }
      // 处理rd数据
      const rds = this.submit.project.rd
      for (const id in rds) {
        for (const u in this.role.rd) {
          if (rds[id] === this.role.rd[u].userid) {
            const name = this.role.rd[u].name
            const email = this.role.rd[u].email
            parameter.project.rd[name] = email
          }
        }
      }
      // 预处理结束
      e.preventDefault()
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log('Received values of form: ', values)
          this.$axios
            .post('/submit/api/v1/save/submit/data', parameter)
            .then(res => {
              if (res.data.status === 0) {
                this.$notification.open({
                  message: '提测成功',
                  description:
                    '提测后平台自动发送邮件给相关人员，测试完成后生成测试报告。',
                })
                this.$router.push({ path: '/submit/' })
              } else {
                this.$notification.error({
                  message: '提测失败',
                  description:
                    '错误' + res.data.status + '：' + res.data.message,
                })
              }
            })
        }
      })
    },
  },
}
</script>
