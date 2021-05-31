<template>
  <div>
    <a-card title="动作事件">
      <a-form :form="form">
        <a-form-item
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 17 }"
          label="选择事件"
        >
          <a-select @change="handleEventChange">
            <a-select-option
              v-for="item in events"
              :key="item.value"
              :value="item.value"
            >
              {{ item.label }}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 17 }"
          label="选择时间"
        >
          <a-date-picker
            @change="handleTimeChangge"
            format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%;"
            show-time
          />
        </a-form-item>
        <a-form-item
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 17 }"
          label="保险师"
        >
          <a-input v-model="event.variables.staff_id" />
        </a-form-item>
        <a-form-item
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 17 }"
          label="用户"
        >
          <a-input
            v-model="event.variables.uuid"
            placeholder="请填写用户UUID"
          />
        </a-form-item>
        <a-form-item
          :label-col="{ span: 5 }"
          :wrapper-col="{ span: 17 }"
          v-if="event.event === 'udesk_call_event'"
          label="电话沟通"
        >
          <a-select @change="handleCallChange">
            <a-select-option
              v-for="item in call"
              :key="item.value"
              :value="item.value"
            >
              {{ item.label }}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-button @click="createEvent" class="button">创建事件</a-button>
      </a-form>
    </a-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      event: {
        variables: {
          event: '',
          event_time: 0,
          uuid: '',
          staff_id: 12,
          created_at: 0,
        },
        event: '',
        event_time: 0,
      },
      events: [
        {
          value: 'ins_leads_first_event',
          label: '首次分配',
        },
        {
          value: 'leads_first_event_udesk_success_48h',
          label: '添加好友',
        },
        {
          value: 'leads_first_event_udesk_30s_48h',
          label: '两次未接通',
        },
        {
          value: 'leads_first_event_udesk_success_48h',
          label: '通话成功',
        },
      ],
      call: [
        {
          value: '客户接听',
          label: '客户接听',
        },
        {
          value: '客户未接',
          label: '客户未接',
        },
      ],
    }
  },
  methods: {
    handleEventChange(value) {
      this.event.event = value
      if (value === 'ins_leads_first_event') {
        this.event.variables.event = 'ins_leads_first_event'
      }
      if (value === 'leads_first_event_udesk_success_48h') {
        this.event.variables.event = 'admin_user_external_friend_event'
      }
      if (value === 'leads_first_event_udesk_30s_48h') {
        this.event.variables.event = 'udesk_call_event'
      }
      if (value === 'leads_first_event_udesk_success_48h') {
        this.event.variables.event = 'udesk_call_event'
      }
    },
    handleTimeChangge(value) {
      this.event.event_time = value.valueOf()
      this.event.variables.event_time = Math.round(value.valueOf() / 1000)
      this.event.variables.created_at = Math.round(value.valueOf() / 1000)
    },
    handleCallChange(value) {
      this.call_result = value
    },
    createEvent() {
      console.log(this.event)
      if (this.event.event === 'udesk_call_event') {
        this.event.call_result = this.call_result
      }
      this.$axios
        .post('/genesis/create/event', this.event)
        .then(res => {
          if (res.data.status === 0) {
            this.$message.info(res.data.message)
          }
        })
        .catch(() => {
          this.$message.info('创建时间出错，请联系刘丽雨！')
        })
    },
  },
}
</script>

<style scoped>
.ant-select {
  width: 100%;
}

.ant-card {
  width: 100%;
}

.ant-form-item-children {
  width: 100%;
}

.button {
  margin-left: 100px;
}
</style>
