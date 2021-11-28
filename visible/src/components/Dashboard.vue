<template>
  <div class="dashboard">
    <cytoscape ref="cy" :config="config" :afterCreated="init_hook">
      <cy-element v-for="element in elements.nodes" :key="element.data.id" :sync=true :definition="element" v-on:click="letbehighlight($event,element)" />
      <cy-element v-for="element in elements.edges" :key="element.data.id" :sync=true :definition="element" v-on:click="letbehighlight($event,element)" />
    </cytoscape>
  </div>
</template>

<script>
import io from 'socket.io-client'

export default {
  name: 'Dashboard',
  data () {
    return {
      config: {
        style: [
          {
            selector: 'node',
            style: {
              'background-color': '#666',
              'label': 'data(id)'
            }
          }, {
            selector: 'edge',
            style: {
              'target-arrow-shape': 'triangle',
              'width': 4,
              'line-color': '#ddd',
              'target-arrow-color': '#ddd'
            }
          }, {
            selector: '.highlighted',
            style: {
              'curve-style': 'bezier',
              'background-color': '#61bffc',
              'line-color': '#61bffc',
              'target-arrow-color': '#61bffc',
              'transition-property': 'background-color, line-color, target-arrow-color',
              'transition-duration': '0.5s',
              'z-index': 1000
            }
          }
        ],
        layout: {
          name: 'grid',
          rows: 2
        }
      },
      elements: {
        nodes: [
        ],
        edges: [
        ]
      },
      socket_io: null
    }
  },
  methods: {
    letbehighlight (cy, element) {
      /*
       * Let the edge be highlighted
       * when the ledger is transporting
       */
      cy.$('#' + element.data.id).toggleClass('highlighted')
      setTimeout(() => {
        cy.$('#' + element.data.id).toggleClass('highlighted')
      }, 800)
    },
    add_highlight (cy, element) {
      /*
       * Add highlight class to the element
       */
      cy.$('#' + element.data.id).addClass('highlighted')
    },
    init_hook (cy) {
      /*
       * initailize the whole graph
       */
      // init the nodes
      let that = this
      this.socket_io = io('ws://127.0.0.1:5000/ws')
      this.axios.get('http://127.0.0.1:5000/user_list').then((response) => {
        for (let i = 0; i < response.data.length; i++) {
          that.elements.nodes.push(
            { data: { id: response.data[i]}, position: {x: 0, y: 0}}
          )
        }
      })

      // init the position
      this.socket_io.on('update_topo', (coordinates) => {
        that.elements.edges = []
        for (let i = 0; i < coordinates.length; i++) {
          coordinates[i].connected_users = JSON.parse(coordinates[i].connected_users)
          cy.$('#' + coordinates[i].user_id).position(coordinates[i].position)
          // init the edges
          for (let j = 0; j < coordinates[i].connected_users.length; j++) {
            that.elements.edges.push(
              { data: { id: coordinates[i].user_id + 'to' + coordinates[i].connected_users[j], source: coordinates[i].user_id, target: coordinates[i].connected_users[j] }}
            )
          }
        }
      })
      this.socket_io.emit('connect_front')

      // set ledger spread listener
      this.socket_io.on('spread_ledger', (data) => {
        let element = null
        for (let i = 0; i < that.elements.edges.length; i++) {
          if (that.elements.edges[i].data.source == data.src &&
                that.elements.edges[i].data.target == data.dest) {
            element = that.elements.edges[i]
          }
        }
        that.letbehighlight(cy, element)
      })

      // set the delegates
      this.socket_io.on('update_delegates', (user_id) => {
          cy.$('.highlighted').removeClass('highlighted')
          for (let i = 0; i < data.length; i++) {
            cy.$('#' + user_id[i]).addClass('highlighted')
          }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
