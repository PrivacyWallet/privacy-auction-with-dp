module.exports = async function(callback) {
let a = accounts[0]
let c = await Calculator.deployed()
await c.set_data(1,"1","2", 10, a)
await c.set_data(1,"1","2", 10, a)
await c.set_data(1,"1","2", 10, a)
await c.set_data(1,"1","2", 10, a)
await c.set_data(1,"1","2", 10, a)
await c.get_data()

}
