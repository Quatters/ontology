<template>
    <div>
        <ModelFields :data="store.data" :model="StatisticsModel" />
    </div>
</template>

<script>
export default {
    components: {
        ModelFields: spa.components.page.ModelFields,
    },
    mixins: [spa.components.BaseViewMixin],
    computed: {
        StatisticsModel() {
            return this.$app.modelsResolver.bySchemaObject(
                this.$app.schema.definitions.Statistics
            );
        },
    },
    mounted() {
        this.store.updateData();
    },
};
</script>

<style scoped>
.title {
    margin: 4px 6px;
}
</style>
