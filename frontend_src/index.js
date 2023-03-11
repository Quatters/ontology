import { ref } from "vue";
import Home from "./Home.vue";

spa.signals.once("allViews.created", ({ views }) => {
    const homeView = new spa.views.View(
        { path: "/", routeName: "home", title: "Home", autoupdate: true },
        null,
        [Home]
    );
    views.set("/", homeView);
    homeView.extendStore((store) => {
        const app = spa.getApp();
        let data = ref({});

        async function updateData() {
            const response = await app.api.makeRequest({
                useBulk: true,
                method: "get",
                path: "statistics",
            });
            if (response.status !== 200) {
                console.warn(response);
                return;
            }
            data.value = response.data;
        }

        return {
            ...store,
            data,
            updateData,
        };
    });
});
