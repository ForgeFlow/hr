/* eslint-disable no-undef */

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {
    Component,
    onMounted,
    onWillStart,
    onWillUnmount,
    useRef,
    useState,
} from "@odoo/owl";
import {ControlPanel} from "@web/search/control_panel/control_panel";
import {standardActionServiceProps} from "@web/webclient/actions/action_service";
import OrgChart from "../lib/orgchart/jquery.orgchart.js";
import html2canvas from "../lib/orgchart/html2canvas.min.js";
import {useSearchBarToggler} from "@web/search/search_bar/search_bar_toggler";

export class HrOrgChartOverview extends Component {
    static template = "HrOrgChartOverview";
    static components = {ControlPanel};
    static props = {...standardActionServiceProps};
    setup() {
        super.setup();
        this.controlPanelDisplay = {};
        this.actionService = useService("action");
        this.searchBarToggler = useSearchBarToggler();
        this.orm = useService("orm");
        this.ui = useService("ui");
        this.orgChartData = {};
        this.chartContainer = useRef("chartContainer");
        this.charDiv = useRef("charDiv");
        this.state = useState({panEnabled: false});
        window.html2canvas = html2canvas;
        onWillStart(async () => {
            Object.assign(
                this.orgChartData,
                await this.orm.call("hr.employee", "get_organization_data")
            );
        });
        onMounted(async () => {
            await this._initOrgChart();
            const el = this.charDiv.el;
            el.addEventListener("click", (ev) => {
                const node = ev.target.closest(".node");
                if (node) {
                    this._onClickNode(ev);
                    return;
                }
                if (ev.target.closest("#print-pdf")) this._onPrintPDF(ev);
                else if (ev.target.closest("#zoom-in")) this._onClickZoomIn(ev);
                else if (ev.target.closest("#zoom-out")) this._onClickZoomOut(ev);
                else if (ev.target.closest("#toggle-pan")) this._onClickTogglePan(ev);
            });
            el.addEventListener("keyup", (ev) => {
                if (ev.target.matches("#key-word")) {
                    this._onKeyUpSearch(ev);
                }
            });
        });

        onWillUnmount(() => {
            if (this.oc) {
                this.chartContainer.el.innerHTML = "";
                this.oc = null;
            }
        });
    }

    _initOrgChart() {
        const container = this.chartContainer.el;
        container.innerHTML = "";
        Object.assign(container.style, {
            width: "100%",
            height: "100%",
            overflow: "auto",
            whiteSpace: "nowrap",
            position: "relative",
        });
        const containerId = this.chartContainer.el.id || "chart-container";
        this.oc = new OrgChart({
            chartContainer: `#${containerId}`,
            data: this.orgChartData,
            nodeContent: "title",
            exportFilename: "MyOrgChart",
            toggleSiblingsResp: true,
            createNode: (node, data) => {
                if (data.image) {
                    const img = document.createElement("img");
                    img.src = `data:image/png;base64,${data.image}`;
                    img.classList.add("avatar");
                    node.insertBefore(img, node.firstChild);
                }
            },
        });
        this._boundPanStart = this.oc._onPanStart.bind(this.oc);
        this._boundPanEnd = this.oc._onPanEnd.bind(this.oc);
    }

    _filterNodes(keyWord) {
        var show = false;
        var $chart = this.$(".orgchart");
        // Disalbe the expand/collapse feture
        $chart.addClass("noncollapsable");
        // Distinguish the matched nodes and the unmatched nodes according to the given key word
        $chart
            .find(".node")
            .filter(function (index, node) {
                $(node).removeClass("matched");
                $(node).removeClass("retained");
                if ($(node).text().toLowerCase().indexOf(keyWord) > -1) {
                    show = true;
                }
                return $(node).text().toLowerCase().indexOf(keyWord) > -1;
            })
            .addClass("matched")
            .closest("table")
            .parents("table")
            .find("tr:first")
            .find(".node")
            .addClass("retained");
        // Hide the unmatched nodes
        $chart.find(".matched,.retained").each(function (index, node) {
            $(node)
                .removeClass("slide-up")
                .closest(".nodes")
                .removeClass("hidden")
                .siblings(".lines")
                .removeClass("hidden");
            var $unmatched = $(node)
                .closest("table")
                .parent()
                .siblings()
                .find(".node:first:not(.matched,.retained)")
                .closest("table")
                .parent()
                .addClass("hidden");
            $unmatched
                .parent()
                .prev()
                .children()
                .slice(1, $unmatched.length * 2 + 1)
                .addClass("hidden");
        });
        // Hide the redundant descendant nodes of the matched nodes
        $chart.find(".matched").each(function (index, node) {
            if (!$(node).closest("tr").siblings(":last").find(".matched").length) {
                $(node).closest("tr").siblings().addClass("hidden");
            }
        });

        if (show) {
            this.$("#chart-container").removeClass("hidden");
        } else {
            this.$("#chart-container").addClass("hidden");
        }
    }

    _clearFilterResults() {
        this.$(".orgchart")
            .removeClass("noncollapsable")
            .find(".node")
            .removeClass("matched retained")
            .end()
            .find(".hidden")
            .removeClass("hidden")
            .end()
            .find(".slide-up, .slide-left, .slide-right")
            .removeClass("slide-up slide-right slide-left");
    }

    async _openEmployeeFormView(id) {
        // Go to the employee form view
        const action = await this.orm.call("hr.employee", "get_formview_action", [
            [id],
        ]);
        this.actionService.doAction(action);
    }

    _onClickNode(ev) {
        ev.preventDefault();
        this._openEmployeeFormView(parseInt(ev.srcElement.parentElement.id));
    }

    async _onPrintPDF(ev) {
        ev.preventDefault();
        const container = this.chartContainer.el.childNodes[0];
        if (!container) return;
        this.ui.block();
        try {
            await new Promise((r) => setTimeout(r, 300));

            const canvas = await html2canvas(container, {
                scale: 2, // Better resolution
                useCORS: true,
            });
            const imgData = canvas.toDataURL("image/png");

            const pdf = new jsPDF({
                orientation: "landscape",
                unit: "pt",
                format: [canvas.width, canvas.height],
            });

            pdf.addImage(imgData, "PNG", 0, 0, canvas.width, canvas.height);
            pdf.save("OrgChart.pdf");
        } catch (err) {
            console.error("PDF export failed:", err);
        } finally {
            this.ui.unblock();
        }
    }

    _onClickZoomIn(ev) {
        ev.preventDefault();
        this.oc._setChartScale(this.oc.chart, 1.1);
    }

    _onClickZoomOut(ev) {
        ev.preventDefault();
        this.oc._setChartScale(this.oc.chart, 0.9);
    }

    _onClickTogglePan(ev) {
        ev.preventDefault();
        if (!this.oc) return;
        const {chart} = this.oc;
        this.state.panEnabled = !this.state.panEnabled;
        if (this.state.panEnabled) {
            chart.addEventListener("mousedown", this._boundPanStart);
            chart.addEventListener("touchstart", this._boundPanStart);
            document.body.addEventListener("mouseup", this._boundPanEnd);
            document.body.addEventListener("touchend", this._boundPanEnd);
            this.chartContainer.el.style.overflow = "hidden";
        } else {
            chart.removeEventListener("mousedown", this._boundPanStart);
            chart.removeEventListener("touchstart", this.oc._onPanStart.bind(this.oc));
            document.body.removeEventListener("mouseup", this._boundPanEnd);
            document.body.removeEventListener("touchend", this._boundPanEnd);
            this.chartContainer.el.style.overflow = "auto";
        }
        const btn = ev.currentTarget.querySelector("#toggle-pan");
        if (btn) btn.classList.toggle("btn-primary", this.state.panEnabled);
    }

    _onKeyUpSearch(ev) {
        var value = ev.target.value.toLowerCase();
        if (value.length === 0) {
            this._clearFilterResults();
        } else {
            this._filterNodes(value);
        }
    }
}

registry.category("actions").add("hr_org_chart_overview", HrOrgChartOverview);
