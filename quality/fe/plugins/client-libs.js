import Vue from 'vue'
import VCharts from 'v-charts'
import echarts from 'echarts' // 引入echarts
import MetaCtrlEnter from 'meta-ctrl-enter'
import Antd from 'ant-design-vue/lib'
import Element from 'element-ui'
import locale from 'element-ui/lib/locale/lang/zh-CN'
import { vuexPlugin } from 'vue-set-get'
import moment from 'moment'

moment.locale('zh-cn')

Vue.use(vuexPlugin)
Vue.use(Element, { locale })

Vue.use(MetaCtrlEnter)
Vue.use(Antd)

Vue.use(VCharts)

Vue.prototype.$echarts = echarts
