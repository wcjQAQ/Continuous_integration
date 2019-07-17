new Vue({
    el:"#vue-AllProject",
    data() {
        return {
          activeName: '',
          modules: '',
          Onemodule: '',
          onlinetags: '',
          testtags: '',
          devtags:''
        };
      },
    methods: {
      listmodules(project) {
        axios
          .get("http://127.0.0.1:5000/api/showmodule/" + project)
          .then(response => (this.modules = response.data));
          this.activeName = project
      },
      listtags() {
        axios
          .get(
            "http://127.0.0.1:5000/api/showtag/" +
              this.activeName +
              "/" +
              this.Onemodule
          )
          .then(response => {
            this.onlinetags = response.data[0]
            this.testtags = response.data[1]
            this.devtags = response.data[2]
          });
          var obj = {
            Project: this.activeName,
            Onemodule: this.Onemodule
        }
    localStorage.setItem('type', JSON.stringify(obj));
    // console.log(obj)
    }
  },
  mounted() {
    var obj = localStorage.getItem('type');
    obj = JSON.parse(obj);
    this.Onemodule = obj.Onemodule
    this.activeName = obj.Project
    console.log(this.activeName,this.Onemodule)
    if (this.Onemodule && this.activeName) {
      axios
      .get(
        "http://127.0.0.1:5000/api/showtag/" +
          this.activeName +
          "/" +
          this.Onemodule
      )
      .then(response => {
        this.onlinetags = response.data[0]
        this.testtags = response.data[1]
        this.devtags = response.data[2]
      });
      axios
      .get("http://127.0.0.1:5000/api/showmodule/" + this.activeName)
      .then(response => (this.modules = response.data));
  }
}

})
