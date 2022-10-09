// pages/local/end/end.js
Page({
  data:{
    score1:'',score2:''
  },
  onLoad:function(){
    this.setData({
      ['score1']:getApp().score[0],
      ['score2']:getApp().score[1]
    })
  },
  btn:function(){
    wx.reLaunch({
      url: '/pages/mode/mode'
    })
  }
})