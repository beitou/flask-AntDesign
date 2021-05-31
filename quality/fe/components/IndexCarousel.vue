<template>
  <a-carousel :afterChange="onChange" effect="fade" autoplay>
    <div v-for="item in images" :key="item.src">
      <a :href="item.src"><img :src="item.img" :alt="item.alt"/></a>
    </div>
  </a-carousel>
</template>
<script>
export default {
  data() {
    return {
      images: [
        {
          src: 'https://quality-qa.xiaobangtouzi.com/',
          img: require('../assets/img/carousel-01.png'),
          alt: 'carousel-01.png',
        },
        {
          src: 'https://quality-qa.xiaobangtouzi.com/genesis/create',
          img: require('../assets/img/carousel-02.png'),
          alt: 'carousel-02.png',
        },
        {
          src: 'https://quality-qa.xiaobangtouzi.com/genesis/delete',
          img: require('../assets/img/carousel-03.png'),
          alt: 'carousel-03.png',
        },
        {
          src: 'https://quality-qa.xiaobangtouzi.com/treasure/index',
          img: require('../assets/img/carousel-04.png'),
          alt: 'carousel-04.png',
        },
      ],
    }
  },
  methods: {
    onChange(a, b, c) {
      console.log(a, b, c)
    },
  },
}
</script>
<style scoped>
/* For demo */
.ant-carousel >>> .slick-slide {
  text-align: center;
  height: 520px;
  line-height: 520px;
  background: #364d79;
  overflow: hidden;
}

.ant-carousel >>> .slick-slide h3 {
  color: #fff;
}

img {
  width: 100%;
}
</style>
