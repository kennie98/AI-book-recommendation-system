<template>
  <div class="container">
    <div class="row">
      <div class="clo-12">
        <p class="display-3">
          Vue Crash course
        </p>
      </div>
    </div>
    <div class="row">
      <AddTodo @on-addtodo="addTodo($event)"/>
    </div>
    <div class="row">
      <div class="col-12 col-lg-6">
        <ur class="list-group">
          <Todo
            v-for="(todo, index) in todos"
            :key="index"
            :todoString="todo.todoString"
            :completed="todo.completed"
            @on-delete="deleteTodo(todo)"
            @on-toggle="toggleTodo(todo)"
            @on-edit="editTodo(todo, $event)"
          />
        </ur>
      </div>
    </div>
  </div>
</template>

<script>
import Todo from "./Todo.vue"
import AddTodo from "./NewTodo"
export default {
  components: {
    Todo,
    AddTodo
  },
  data() {
    return {
      todos: [
        {todoString: "complete AI server", completed: true},
        {todoString: "complete manager logic", completed: true},
        {todoString: "run and test on Kubernetes", completed: true},
        {todoString: "learn Vue.Js", completed: false},
        {todoString: "complete browser part", completed: false},
        {todoString: "finish Demo", completed: false},
        {todoString: "write report", completed: false},
      ]
    }
  },
  methods: {
    addTodo(newTodo){
      this.todos.push({
        todoString: newTodo,
        completed: false
      })
    },
    toggleTodo(todo){
      todo.completed = !todo.completed;
    },
    editTodo(todo, newTodoString) {
      todo.todoString = newTodoString;
    },
    deleteTodo(deleteTodo) {
      this.todos = this.todos.filter(
        todo =>todo.todoString !== deleteTodo.todoString
      )
    }
  }
}
</script>

<style>

</style>