import{r as o,_ as e,e as t,t as n,n as i,a as s,y as a}from"./index-02aff447.js";import"./c.235f0fef.js";import{a as c}from"./c.552cfd34.js";import"./c.0cab7b14.js";import"./c.79c6012c.js";import"./c.4e4be3f1.js";let r=class extends s{render(){return a`
      <esphome-process-dialog
        .heading=${`Download ${this.configuration}`}
        .type=${"compile"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${void 0===this._result?"":0===this._result?a`
              <a
                slot="secondaryAction"
                href="${`./download.bin?configuration=${encodeURIComponent(this.configuration)}`}"
              >
                <mwc-button label="Download"></mwc-button>
              </a>
            `:a`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_handleProcessDone(o){if(this._result=o.detail,0!==o.detail)return;const e=document.createElement("a");e.download=this.configuration+".bin",e.href=`./download.bin?configuration=${encodeURIComponent(this.configuration)}`,document.body.appendChild(e),e.click(),e.remove()}_handleRetry(){c(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};r.styles=o`
    a {
      text-decoration: none;
    }
  `,e([t()],r.prototype,"configuration",void 0),e([n()],r.prototype,"_result",void 0),r=e([i("esphome-compile-dialog")],r);
