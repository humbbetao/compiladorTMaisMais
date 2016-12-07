; ModuleID = "Programa"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare float @"escrevaFlutuante"(float %".1") 

declare i32 @"escrevaInteiro"(i32 %".1") 

declare float @"leiaFlutuante"() 

declare i32 @"leiaInteiro"() 

@"global.n" = external global i32
define i32 @"fatorial"(i32 %"n") 
{
entry:
  %"n.1" = alloca i32
  store i32 %"n", i32* %"n.1"
  %".4" = load i32, i32* %"n.1"
  %"fatorial.fat" = alloca i32
  %".5" = load i32, i32* %"n.1"
  %".6" = sitofp i32 %".5" to float
  %"fcmpMaior" = fcmp ugt float %".6",              0x0
  br i1 %"fcmpMaior", label %"entao", label %"senao"
entao:
  %".8" = fptosi float 0x3ff0000000000000 to i32
  store i32 %".8", i32* %"fatorial.fat"
  %".10" = load i32, i32* %"fatorial.fat"
  %".11" = sitofp i32 %".10" to float
  br label %"fim"
senao:
  %".13" = fptosi float 0x4000000000000000 to i32
  store i32 %".13", i32* %"fatorial.fat"
  %".15" = load i32, i32* %"fatorial.fat"
  %".16" = sitofp i32 %".15" to float
  br label %"fim"
fim:
  %"seTmp" = phi float [%".11", %"entao"], [%".16", %"senao"]
  %".18" = load i32, i32* %"fatorial.fat"
  %".19" = sitofp i32 %".18" to float
  %".20" = fptosi float %".19" to i32
  ret i32 %".20"
}

define i32 @"main"() 
{
entry:
  %"leiaFlutuante" = call float () @"leiaFlutuante"()
  %".2" = fptosi float %"leiaFlutuante" to i32
  store i32 %".2", i32* @"global.n"
  %".4" = load i32, i32* @"global.n"
  %".5" = load i32, i32* @"global.n"
  %".6" = sitofp i32 %".5" to float
  %".7" = fptosi float %".6" to i32
  %".8" = call i32 (i32) @"fatorial"(i32 %".7")
  %".9" = call i32 (i32) @"escrevaInteiro"(i32 %".8")
  %".10" = fptosi float              0x0 to i32
  ret i32 %".10"
}
