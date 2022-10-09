// pages/mode/mode.js
Page({
  btn_local(){
    wx.navigateTo({
      url: '../local/local',
    })
  },
  btn_ai(){
    wx.navigateTo({
      url: '../ai/ai',
    })
  },
  btn_online(){
    wx.navigateTo({
      url: '../online/online',
    })
  }
})