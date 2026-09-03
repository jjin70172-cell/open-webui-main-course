<script lang="ts">
	import { onMount } from 'svelte';

	import { showSidebar } from '$lib/stores';
	import { getHelpDocument } from '$lib/apis';

	import Markdown from '$lib/components/chat/Messages/Markdown.svelte';
	import Spinner from '$lib/components/common/Spinner.svelte';

	let loaded = false;
	let error: any = null;
	let doc: any = null;

	onMount(async () => {
		try {
			doc = await getHelpDocument(localStorage.token);
		} catch (e) {
			error = e;
		}
		loaded = true;
	});
</script>

<div
	class="flex flex-col w-full h-screen max-h-[100dvh] transition-width duration-200 ease-in-out {$showSidebar
		? 'md:max-w-[calc(100%-var(--sidebar-width))]'
		: ''} max-w-full"
>
	<div class="w-full max-w-4xl mx-auto p-6 overflow-y-auto">
		{#if !loaded}
			<div class="flex justify-center items-center py-20">
				<Spinner />
			</div>
		{:else if error || !doc}
			<div class="text-center text-gray-500 py-20">帮助文档加载失败，请稍后重试。</div>
		{:else}
			<h1 class="text-2xl font-bold mb-4">{doc.title}</h1>
			<div class="text-xs text-gray-400 mb-6">
				来源：{doc.source}
			</div>
			<div class="prose dark:prose-invert max-w-none">
				<Markdown content={doc.content} />
			</div>
		{/if}
	</div>
</div>
