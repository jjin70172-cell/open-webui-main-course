<script lang="ts">
	import { getContext } from 'svelte';

	import { getHelpDocument } from '$lib/apis';
	import Markdown from '$lib/components/chat/Messages/Markdown.svelte';
	import Modal from '$lib/components/common/Modal.svelte';
	import Spinner from '$lib/components/common/Spinner.svelte';
	import XMark from '$lib/components/icons/XMark.svelte';

	const i18n = getContext('i18n');

	export let show = false;

	type HelpDocument = {
		title: string;
		content: string;
		source: string;
		updated_at: number;
	};

	let loading = false;
	let loaded = false;
	let error = false;
	let doc: HelpDocument | null = null;

	const load = async () => {
		if (loading) {
			return;
		}

		loading = true;
		error = false;
		doc = await getHelpDocument(localStorage.token).catch(() => null);

		if (!doc) {
			error = true;
		}

		loading = false;
		loaded = true;
	};

	$: if (show && !loaded) {
		load();
	}
</script>

<Modal bind:show size="lg" className="bg-white dark:bg-gray-900 rounded-3xl overflow-hidden">
	<div class="flex max-h-[70vh] flex-col">
		<div
			class="flex shrink-0 items-start justify-between gap-4 px-4 pb-2.5 pt-3.5 text-black dark:text-white"
		>
			<div class="min-w-0">
				<h2 class="m-0 truncate text-base font-normal">系统帮助文档</h2>
				{#if doc}
					<div class="mt-1 flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400">
						<span>{$i18n.t('Source')}: {doc.source}</span>
					</div>
				{/if}
			</div>

			<button
				class="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-gray-400 transition hover:bg-gray-100 hover:text-gray-700 dark:text-gray-500 dark:hover:bg-white/10 dark:hover:text-gray-200"
				on:click={() => {
					show = false;
				}}
				aria-label={$i18n.t('Close')}
			>
				<XMark className="size-4" />
			</button>
		</div>

		<div
			class="min-h-0 flex-1 overflow-y-auto px-4 py-2 text-gray-700 scrollbar-hidden dark:text-gray-100"
		>
			{#if loading}
				<div class="flex items-center justify-center py-16 text-sm">
					<Spinner />
				</div>
			{:else if error}
				<div class="py-16 text-center text-sm text-gray-500 dark:text-gray-400">
					帮助文档加载失败，请稍后重试。
				</div>
			{:else if doc}
				<div class="prose dark:prose-invert max-w-none">
					<Markdown content={doc.content} />
				</div>
			{/if}
		</div>
	</div>
</Modal>
