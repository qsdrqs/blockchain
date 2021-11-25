<template>
  <div class="dashboard">
    <cytoscape ref="cy" :config="config" >
      <cy-element v-for="element in elements.nodes" :key="element.data.id" :sync=true :definition="element" v-on:click="letbehighlight($event,element)" />
      <cy-element v-for="element in elements.edges" :key="element.data.id" :sync=true :definition="element" v-on:click="letbehighlight($event,element)" />
    </cytoscape>
  </div>
</template>

<script>

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
              'background-color': '#61bffc',
              'line-color': '#61bffc',
              'target-arrow-color': '#61bffc',
              'transition-property': 'background-color, line-color, target-arrow-color',
              'transition-duration': '0.5s'
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
          { data: { id: 'a'}},
          { data: { id: 'b'}},
          { data: { id: 'c'}},
          { data: { id: 'd'}},
          { data: { id: 'e'}},
          { data: { id: 'f'}}
        ],
        edges: [
          { data: { id: 'ae', source: 'a', target: 'e' } },
          { data: { id: 'ab', source: 'a', target: 'b' } },
          { data: { id: 'be', source: 'b', target: 'e' } },
          { data: { id: 'bc', source: 'b', target: 'c' } },
          { data: { id: 'ce', source: 'c', target: 'e' } },
          { data: { id: 'cd', source: 'c', target: 'd' } },
          { data: { id: 'de', source: 'd', target: 'e' } }
        ]
      }
    }
  },
  mounted () {
    for (let i = 0; i < this.elements.nodes.length; i++) {
      this.elements.nodes[i].position = {x: Math.random() * 1000, y: Math.random() * 500 + 100}
    }
  },
  methods: {
    letbehighlight (event, element) {
      event.cy.$("#"+element.data.id).toggleClass('highlighted');
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
