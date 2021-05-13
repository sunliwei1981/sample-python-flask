<template>
	<view class="content" :style="{'backgroundColor': color_style.background_color, 'color': color_style.color}">
		<view class="input-group">
			<view class="input-row border" :style="{'borderColor': color_style.bg_2 }">
				<text class="title">{{$t("me.email")}}:</text>
				<m-input class="m-input" type="email" clearable v-model="email" :placeholder='$t("me.email_placeholder")'></m-input>
			</view>
			<view class="input-row border" :style="{'borderColor': color_style.bg_2 }">
				<text class="title">{{$t("me.password")}}:</text>
				<m-input type="password" displayable v-model="password" :placeholder='$t("me.password_placeholder")'></m-input>
			</view>
		</view>
		
		<view class="btn-row">
			<button type="default"  :class="{'default': !color_style.style_id}" @tap="bindLogin">{{$t("me.login")}}</button>
		</view>
		
		<view class="action-row">
			<navigator url="../common/reg" :style="{'color': color_style.color_2 }">{{$t("me.register_acount")}}</navigator>
			<navigator url="../common/pwd" :style="{'color': color_style.color_2 }">{{$t("me.reset_password")}}</navigator>
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
	import user_service from "@/common/libs/user.js";
	export default {
		computed: mapState(['user_id', 'user_name', 'user_token', 'has_login', 'color_style']),
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

			bindLogin() {
				this.email = this.email.replace(/\s+/g, "");
				if (!user_service.email_check(this.email)) {
					// #ifdef APP-PLUS
					plus.nativeUI.toast(this.$t("me.email_not_available"));
					// #endif				    
					return;
				}
				if (this.password.length < 6) {
					// #ifdef APP-PLUS
					plus.nativeUI.toast(this.$t("me.password_must_6"));
					// #endif                    
					return;
				}
				// #ifdef APP-PLUS
				plus.nativeUI.showWaiting(this.$t("common.logging_in"));
				// #endif	

				var req = {};
				req.url = configs.server_url + "/user/email_login/";
				req.dataType = 'json';
				req.data = {
					email: this.email.trim().toLowerCase(),
					password: this.password,
					user_type: this.app_type
				};

				// register pushid
				// #ifdef APP-PLUS
				req.data.platform = plus.os.name.toLowerCase();
				if (req.data.platform == "ios") {
					var client_info = plus.push.getClientInfo();
					req.data.push_cid = client_info.clientid;
					req.data.push_token = client_info.token;
				}
				// #endif

				req.method = "POST"
				req.success = (res) => {
					if (res.data.valid_user) {
						// set login state
						this.$store.state.user_id = res.data.user_id;
						this.$store.state.user_name = res.data.user_name;
						this.$store.state.email = res.data.email;
						this.$store.state.user_token = res.data.user_token;
						this.$store.state.user_addr = res.data.user_addr;
						this.$store.state.has_login = true;

						// Write to local cache
						uni.setStorageSync("has_login", true);
						uni.setStorageSync("user_id", res.data.user_id);
						uni.setStorageSync("user_name", res.data.user_name);
						uni.setStorageSync("email", res.data.email);
						uni.setStorageSync("user_token", res.data.user_token);
						uni.setStorageSync("user_addr", res.data.user_addr);
						// Cache client version number
						uni.setStorageSync("version", configs.version);

						// #ifdef APP-PLUS
						plus.nativeUI.closeWaiting();
						plus.nativeUI.toast(this.$t("common.logging_in_status_1"));
						// #endif							
						setTimeout(() => {
							uni.navigateBack();
						}, 1000);


					} else {
						// #ifdef APP-PLUS
						plus.nativeUI.closeWaiting();
						plus.nativeUI.toast(this.$t("common.logging_in_status_0"));
						// #endif							
					}
				};
				req.fail = (res) => {
					// #ifdef APP-PLUS
					plus.nativeUI.closeWaiting();
					plus.nativeUI.toast(this.$t("common.loading_communication_fail"));
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
