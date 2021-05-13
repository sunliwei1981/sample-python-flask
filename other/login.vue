<template>
	<view class="content" :style="{'backgroundColor': colorStyle.backgroundColor, 'color': colorStyle.color}">
		<view class="input-group">
			<view class="input-row border" :style="{'borderColor': colorStyle.bg2 }">
				<text class="title">{{$t("me.email")}}:</text>
				<m-input class="m-input" type="email" clearable v-model="email" :placeholder='$t("me.emailPlaceholder")'></m-input>
			</view>
			<view class="input-row border" :style="{'borderColor': colorStyle.bg2 }">
				<text class="title">{{$t("me.password")}}:</text>
				<m-input type="password" displayable v-model="password" :placeholder='$t("me.passwordPlaceholder")'></m-input>
			</view>
		</view>
		
		<view class="btn-row">
			<button type="default"  :class="{'default': !colorStyle.styleId}" @tap="emailLogin">{{$t("me.login")}}</button>
		</view>
		
		<view class="action-row">
			<navigator url="../common/reg" :style="{'color': colorStyle.color2 }">{{$t("me.registerAcount")}}</navigator>
			<navigator url="../common/pwd" :style="{'color': colorStyle.color2 }">{{$t("me.resetPassword")}}</navigator>
		</view>
		
	</view>
</template>

<script>
	import configs from "@/common/config.js";
	import {
		mapState,
		mapMutations
	} from 'vuex';
	import mInput from '@/components/m-input.vue';
	import userService from "@/common/libs/user.js";
	export default {
		computed: mapState(['userId', 'userName', 'userToken', 'hasLogin', 'colorStyle']),
		components: {
			mInput
		},
		data() {
			return {
				email: '',
				password: '',
			}
		},

		methods: {

			emailLogin() {
				this.email = this.email.replace(/\s+/g, "");
				if (!userService.emailCheck(this.email)) {
					// #ifdef APP-PLUS
					plus.nativeUI.toast(this.$t("me.emailNotAvailable"));
					// #endif				    
					return;
				}
				if (this.password.length < 6) {
					// #ifdef APP-PLUS
					plus.nativeUI.toast(this.$t("me.passwordMust6"));
					// #endif                    
					return;
				}
				// #ifdef APP-PLUS
				plus.nativeUI.showWaiting(this.$t("common.loggingIn"));
				// #endif	

				var req = {};
				req.url = configs.serverUrl + "/user/email_login/";
				req.dataType = 'json';
				req.data = {
					email: this.email.trim().toLowerCase(),
					password: this.password,
					userType: this.appType
				};

				// register pushid
				// #ifdef APP-PLUS
				req.data.platform = plus.os.name.toLowerCase();
				if (req.data.platform == "ios") {
					var clientInfo = plus.push.getClientInfo();
					req.data.pushCid = clientInfo.clientid;
					req.data.pushToken = clientInfo.token;
				}
				// #endif

				req.method = "POST"
				req.success = (res) => {
					if (res.data.validUser) {
						// set login state
						this.$store.state.userId = res.data.userId;
						this.$store.state.userName = res.data.userName;
						this.$store.state.email = res.data.email;
						this.$store.state.userToken = res.data.userToken;
						this.$store.state.userAddr = res.data.userAddr;
						this.$store.state.hasLogin = true;

						// Write to local cache
						uni.setStorageSync("hasLogin", true);
						uni.setStorageSync("userId", res.data.userId);
						uni.setStorageSync("userName", res.data.userName);
						uni.setStorageSync("email", res.data.email);
						uni.setStorageSync("userToken", res.data.userToken);
						uni.setStorageSync("userAddr", res.data.userAddr);
						// Cache client version number
						uni.setStorageSync("version", configs.version);

						// #ifdef APP-PLUS
						plus.nativeUI.closeWaiting();
						plus.nativeUI.toast(this.$t("common.loggingInStatus1"));
						// #endif							
						setTimeout(() => {
							uni.navigateBack();
						}, 1000);


					} else {
						// #ifdef APP-PLUS
						plus.nativeUI.closeWaiting();
						plus.nativeUI.toast(this.$t("common.loggingInStatus0"));
						// #endif							
					}
				};
				req.fail = (res) => {
					// #ifdef APP-PLUS
					plus.nativeUI.closeWaiting();
					plus.nativeUI.toast(this.$t("common.loadingCommunicationFail"));
					// #endif
				}
				uni.request(req);
			},
			
		},
		onLoad() {
			uni.setNavigationBarTitle({
				title: this.$t("me.login")
			});
		},

	}
</script>

<style>
	@import url("login.css");
</style>
