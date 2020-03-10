<template>
<div class="chart">
	<h3 v-if="title">{{ title }}</h3>
	<p v-if="description" class="text-gray text-center mb-2">{{ description }}</p>
	<div v-for="r in 7" :key="r" class="row">
		<div class="legend mr-1 text-gray text-xs text-mono">{{ weekdays[r-1] }}</div>
		<div
			v-for="c in 24"
			:key="c"
			:style="'background: rgba(' + rgb + ', ' + dataset[r-1][c-1]/mailsPerWeekdayPerHourMax + ')'"
			:data-tooltip="weekdays[r-1] + ', ' + (c-1) + ':00\n' + dataset[r-1][c-1] + ' mails'"
			class="cell tooltip"
		></div>
	</div>
	<div class="row">
		<div class="legend mr-1 text-gray text-xs text-mono"></div>
		<div v-for="c in 24" :key="c"  class="legend mt-1 text-gray text-sm text-center">
			<span v-if="c%2==1">{{c-1}}</span>
		</div>
	</div>
</div>
</template>

<script>
export default {
	props: {
		title: String,
		description: String,
		rgb: String,
		dataset: Object,
	},
	computed: {
		mailsPerWeekdayPerHourMax () {
			let max = 0
			for (let d in this.dataset) {
				let m = Math.max(...this.dataset[d])
				max = m > max ? m : max
			}
			return max
		},
		weekdays () {
			return ['Mo','Tu','We','Th','Fr','Sa','Su']
		}
	}
}
</script>

<style lang="stylus">
.heatmap
	.row
		display flex
		.cell, .legend
			height 20px
			width calc(100%/8)
			transition background .8s ease
</style>
