import{r as t,_ as o,e,t as s,n as i,a,y as n}from"./index-02aff447.js";import"./c.235f0fef.js";import{g as r}from"./c.0cab7b14.js";import{a2 as c}from"./c.4e4be3f1.js";const l=(t,o)=>{import("./c.9035bca5.js");const e=document.createElement("esphome-logs-dialog");e.configuration=t,e.target=o,document.body.append(e)};let p=class extends a{render(){return this._ports?n`
      <mwc-dialog
        open
        heading=${"Show Logs"}
        scrimClickAction
        @closed=${this._handleClose}
      >
        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          .port=${"OTA"}
          @click=${this._pickPort}
        >
          <span>Connect wirelessly</span>
          <span slot="secondary">Requires the device to be online</span>
          ${c}
        </mwc-list-item>

        ${this._ports.map((t=>n`
            <mwc-list-item
              twoline
              hasMeta
              dialogAction="close"
              .port=${t.port}
              @click=${this._pickPort}
            >
              <span>${t.desc}</span>
              <span slot="secondary">${t.port}</span>
              ${c}
            </mwc-list-item>
          `))}

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      </mwc-dialog>
    `:n``}firstUpdated(t){super.firstUpdated(t),r().then((t=>{this._ports=t}))}_pickPort(t){l(this.configuration,t.currentTarget.port)}_handleClose(){this.parentNode.removeChild(this)}};p.styles=t`
    :host {
      --mdc-theme-primary: #03a9f4;
    }

    mwc-list-item {
      margin: 0 -20px;
    }
  `,o([e()],p.prototype,"configuration",void 0),o([s()],p.prototype,"_ports",void 0),p=o([i("esphome-logs-target-dialog")],p);var m=Object.freeze({__proto__:null});export{m as l,l as o};
