<template>
  <div>
    <a-row>
      <a-col :span="8">
        <a-form-item
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 19 }"
          label="UUID"
        >
          <a-input-search v-model="uuid" placeholder="请输入关键词搜索" />
        </a-form-item>
      </a-col>
      <a-col :span="8">
        <a-form-item
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 19 }"
          label="业务"
        >
          <a-select @change="handleBusinessChange" default-value="基础">
            <a-select-option
              v-for="item in business"
              :key="item.label"
              :value="item.value"
            >
              {{ item.label }}
            </a-select-option>
          </a-select>
        </a-form-item>
      </a-col>
      <a-col :span="8">
        <a-form-item
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 19 }"
          label="事件"
        >
          <a-select
            @change="handleEventChange"
            @search="handleEventSearch"
            :filterOption="false"
            default-value="all"
            mode="multiple"
          >
            <a-select-option
              v-for="item in event"
              :key="item.name"
              :value="item.event_sn"
            >
              {{ item.name }}
            </a-select-option>
          </a-select>
        </a-form-item>
      </a-col>
    </a-row>
    <a-row>
      <a-col :span="8">
        <a-form-item
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 19 }"
          label="上报时间"
        >
          <a-range-picker
            @change="onChange"
            :showTime="{
              hideDisabledOptions: true,
              defaultValue: [
                moment('00:00', 'HH:mm'),
                moment('23:59', 'HH:mm'),
              ],
            }"
            format="YYYY-MM-DD HH:mm"
          />
        </a-form-item>
      </a-col>
      <a-col :span="8">
        <a-form-item
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 19 }"
          label="环境"
        >
          <a-select @change="handleEnvironmentChange" default-value="qa">
            <a-select-option value="qa">测试</a-select-option>
            <a-select-option value="staging">预发</a-select-option>
            <a-select-option value="production">正式</a-select-option>
          </a-select>
        </a-form-item>
      </a-col>
      <a-col :span="8">
        <a-button @click="startTesting" type="primary" class="start">
          开始测试
        </a-button>
      </a-col>
    </a-row>
    <a-row>
      <a-divider />
    </a-row>
    <a-row>
      <a-col :span="16">
        <a-row>
          <a-button
            @click="startTesting"
            v-if="visiable"
            type="primary"
            class="refresh"
          >
            刷新
          </a-button>
        </a-row>
        <a-timeline>
          <a-timeline-item v-for="item in data" :key="item.index">
            <a-row>
              <a-col :span="1">
                <span class="time">{{ item.time }}</span>
              </a-col>
              <a-col :span="23">
                <span @click="clickEvent(item)" class="content">
                  {{ item.content }}
                </span>
              </a-col>
            </a-row>
          </a-timeline-item>
        </a-timeline>
        <a-button
          @click="fetchMore"
          v-if="visiable"
          type="primary"
          class="more"
        >
          更多
        </a-button>
      </a-col>
      <a-col :span="8">
        <a-card v-if="visiable" title="自定义变量">
          <pre><code>{{ custom }}</code></pre>
        </a-card>
        <a-card v-if="visiable" title="预定义变量">
          <pre><code>{{ this.default }}</code></pre>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import moment from 'moment'
export default {
  data() {
    return {
      index: 0,
      env: 'qa',
      team: 'BASIS',
      event: [],
      business: [],
      eventMapping: {},
      uuid: '',
      limit: 10,
      offset: 0,
      eventSn: ['all'],
      start: 0,
      end: 0,
      data: [],
      custom: {},
      default: {},
    }
  },
  computed: {
    visiable: function() {
      return !(
        Array.prototype.isPrototypeOf(this.data) && this.data.length === 0
      )
    },
  },
  mounted() {
    this.start = 0
    this.getBusiness()
    this.getEvent()
  },
  methods: {
    moment,
    getUrl() {
      if (this.env === 'production') {
        return 'https://api.xiaobangtouzi.com/data-api/report'
      } else if (this.env === 'staging') {
        return 'https://api-staging.xiaobangtouzi.com/data-api/report'
      } else {
        return 'https://api-qa.xiaobangtouzi.com/data-api/report'
      }
    },
    getBusiness() {
      const url = this.getUrl()
      this.$axios
        .post(url, {
          reqParams: 'track_event_business',
          sqlRarams: {},
        })
        .then(res => {
          this.business = []
          for (const i in res.data.data) {
            let zh = ''
            const en = res.data.data[i].business
            if (en === 'BASIS') {
              zh = '基础'
            } else if (en === 'INSURANCE') {
              zh = '保险'
            } else if (en === 'FQ') {
              zh = '财商'
            } else {
              zh = '不知道怎么处理'
            }
            this.business.push({
              value: en,
              label: zh,
            })
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    getEvent() {
      const url = this.getUrl()
      this.$axios
        .post(url, {
          reqParams: 'track_event_sn',
          sqlRarams: {
            business: this.team,
          },
        })
        .then(res => {
          const all = [{ name: '全部', event_sn: 'all' }]
          this.event = all.concat(res.data.data)

          this.eventMapping = {}
          for (const i in res.data.data) {
            const name = res.data.data[i].name
            const event_sn = res.data.data[i].event_sn
            this.eventMapping[event_sn] = name
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    handleEnvironmentChange(value) {
      this.env = value
      this.getBusiness()
    },
    handleEventChange(value) {
      // console.log(value)
      // if (value.includes('all') && value.length > 1) {
      //   value = value.filter(v => v !== 'all')
      // }
      this.offset = 0
      this.eventSn = value
      console.log(this.eventSn)
    },
    handleEventSearch(value) {
      console.log('search ' + value + ' ...')
      const url = this.getUrl()
      this.$axios
        .post(url, {
          reqParams: 'track_event_sn',
          sqlRarams: {
            business: this.team,
          },
        })
        .then(res => {
          this.event = res.data.data.filter(
            item => item.name.includes(value) || item.event_sn.includes(value)
          )
          console.log(this.event)
        })
        .catch(error => {
          console.log(error)
        })
    },
    handleBusinessChange(value) {
      this.offset = 0
      this.team = value
      this.getEvent()
    },
    startTesting() {
      this.index = 0
      this.data = []
      const url = this.getUrl()
      const params = {
        startTime: this.start,
        endTime: this.end || new Date().getTime(),
        offset: this.offset * this.limit,
        limit: this.limit,
        uuid: this.uuid,
      }
      if (this.eventSn.includes('all') || this.eventSn.length === 0) {
        const eventSn = []
        for (const sn in this.eventMapping) {
          if (this.eventMapping.hasOwnProperty(sn)) {
            eventSn.push(sn)
          }
        }
        params.eventSn = eventSn.join(',')
      } else {
        params.eventSn = this.eventSn.join(',')
      }
      this.$axios
        .post(url, {
          reqParams: 'track_event_top',
          sqlRarams: params,
        })
        .then(res => {
          console.log(res.data.data)
          if (
            Array.prototype.isPrototypeOf(res.data.data) &&
            res.data.data.length === 0
          ) {
            this.$message.info('啥都没有查到！')
          } else {
            console.log(this.eventMapping)
            for (const i in res.data.data) {
              const time = this.timestampToString(res.data.data[i].sendingTime)
              const name = this.eventMapping[res.data.data[i].eventSn]
              const event = res.data.data[i].eventSn
              const eventVariable = res.data.data[i].eventVariable
              const defaultVariable = res.data.data[i].defaultVariable
              console.log(res.data.data[i].eventSn)
              const content = '显示名：' + name + '\t标志符：' + event
              this.data.push({
                index: this.index,
                time: time,
                name: name,
                event: event,
                content: content,
                custom: eventVariable,
                default: defaultVariable,
              })
              this.index += 1
            }
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    fetchMore() {
      this.offset = this.offset + 1
      const url = this.getUrl()
      const params = {
        startTime: this.start,
        endTime: this.end || new Date().getTime(),
        offset: this.offset * this.limit,
        limit: this.limit,
        uuid: this.uuid,
      }
      if (this.eventSn.includes('all') || this.eventSn.length === 0) {
        const eventSn = []
        for (const sn in this.eventMapping) {
          if (this.eventMapping.hasOwnProperty(sn)) {
            eventSn.push(sn)
          }
        }
        params.eventSn = eventSn.join(',')
      } else {
        params.eventSn = this.eventSn.join(',')
      }
      this.$axios
        .post(url, {
          reqParams: 'track_event_top',
          sqlRarams: params,
        })
        .then(res => {
          if (
            Array.prototype.isPrototypeOf(res.data.data) &&
            res.data.data.length === 0
          ) {
            this.$message.info('啥都没有查到！')
          } else {
            for (const i in res.data.data) {
              const time = this.timestampToString(res.data.data[i].sendingTime)
              const name = this.eventMapping[res.data.data[i].eventSn]
              const event = res.data.data[i].eventSn
              const eventVariable = res.data.data[i].eventVariable
              const defaultVariable = res.data.data[i].defaultVariable
              const content = '显示名：' + name + '\t标志符：' + event
              this.data.push({
                time: time,
                name: name,
                event: event,
                content: content,
                custom: eventVariable,
                default: defaultVariable,
              })
            }
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    clickEvent(value) {
      this.custom = JSON.stringify(JSON.parse(value.custom), null, 4)
      this.default = JSON.stringify(JSON.parse(value.default), null, 4)
    },
    onChange(date, dateString) {
      this.start = new Date(dateString[0]).getTime()
      this.end = new Date(dateString[1]).getTime()
    },
    timestampToString(timestamp) {
      const time = new Date(timestamp)
      const Y = time.getFullYear()
      const M = (time.getMonth() + 1).toString().padStart(2, '0')
      const D = time
        .getDate()
        .toString()
        .padStart(2, '0')
      const h = time
        .getHours()
        .toString()
        .padStart(2, '0')
      const m = time
        .getMinutes()
        .toString()
        .padStart(2, '0')
      const s = time
        .getSeconds()
        .toString()
        .padStart(2, '0')
      return `${Y}/${M}/${D} ${h}:${m}:${s}`
    },
  },
}
</script>

<style scoped>
.refresh {
  margin-bottom: 20px;
}

.more {
  margin-top: -60px;
}

.time {
  margin-left: -180px;
}

.content {
  padding-right: 200px;
}

.ant-timeline {
  padding-left: 160px;
}

.ant-input {
  width: 100%;
}

.ant-select {
  width: 100%;
}

.ant-card {
  margin-bottom: 20px;
  width: 450px;
}

.start {
  margin-left: 50px;
}
</style>
