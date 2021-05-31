<template functional>
  <a-sub-menu :key="props.menuInfo.uuid">
    <span slot="title">
      <a-icon type="setting" style="horizontal-align: middle" />
      <span>{{ props.menuInfo.title }}</span>
    </span>
    <template v-for="item in props.menuInfo.children">
      <a-menu-item
        v-if="!item.children"
        :key="item.uuid"
        @click="() => parent.$router.push({ path: item.path })"
      >
        <span>{{ item.title }}</span>
      </a-menu-item>
      <sub-menu v-else :key="item.uuid" :menu-info="item" />
    </template>
  </a-sub-menu>
</template>
<script>
export default {
  props: ['menuInfo'],
}
</script>
