new Vue({
    el:"#vue-AllProject",
    data () {
        return {
          info: null,
          project:"test",
          module:"master",
          tags: null
        }
    },
    methods: {
        OneTags: function(project,module){
            this.project = project;
            this.module = module;
            axios
                .get('http://127.0.0.1:5000/api/showtag/' + this.project + '/' + this.module )
                .then(response => (this.tags = response.data))
            var obj = {
                project: project,
                module: module  
            }

            localStorage.setItem('type', JSON.stringify(obj));
        }
    },
    mounted () {

        var obj = localStorage.getItem('type');

        obj = JSON.parse(obj);

        axios
            .get('http://127.0.0.1:5000/api/showproject')
            .then(response => (this.info = response.data))

        axios
            .get('http://127.0.0.1:5000/api/showtag/' + obj.project + '/' + obj.module )
            .then(response => (this.tags = response.data))
    }
});

