#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float32.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/float32.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/include/builtins/abs.hpp>
#include <pythonic/include/builtins/enumerate.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/int_.hpp>
#include <pythonic/include/builtins/len.hpp>
#include <pythonic/include/builtins/pythran/make_shape.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/round.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/zeros.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/floordiv.hpp>
#include <pythonic/include/operator_/ge.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/ne.hpp>
#include <pythonic/include/operator_/neg.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/slice.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/abs.hpp>
#include <pythonic/builtins/enumerate.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/int_.hpp>
#include <pythonic/builtins/len.hpp>
#include <pythonic/builtins/pythran/make_shape.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/round.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/zeros.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/floordiv.hpp>
#include <pythonic/operator_/ge.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/ne.hpp>
#include <pythonic/operator_/neg.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/slice.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_spatiotemporal_spectra
{
  struct __transonic__
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef pythonic::types::str __type0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type0>()))>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct compute_spectrum_kzkhomega
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type0>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type2;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type5;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type6;
      typedef std::integral_constant<long,1> __type8;
      typedef indexable_container<__type8, typename std::remove_reference<__type3>::type> __type9;
      typedef typename __combined<__type2,__type9>::type __type10;
      typedef typename pythonic::assignable<decltype(std::declval<__type6>()(std::declval<__type10>()))>::type __type11;
      typedef indexable_container<__type8, typename std::remove_reference<__type1>::type> __type13;
      typedef typename __combined<__type0,__type13>::type __type14;
      typedef typename pythonic::assignable<decltype(std::declval<__type6>()(std::declval<__type14>()))>::type __type15;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type16;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type16>())) __type17;
      typedef typename pythonic::assignable<typename std::tuple_element<2,typename std::remove_reference<__type17>::type>::type>::type __type18;
      typedef long __type19;
      typedef decltype(pythonic::operator_::add(std::declval<__type18>(), std::declval<__type19>())) __type20;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::functor::floordiv()(std::declval<__type20>(), std::declval<__type19>()))>::type __type21;
      typedef decltype(std::declval<__type5>()(std::declval<__type11>(), std::declval<__type15>(), std::declval<__type21>())) __type22;
      typedef typename pythonic::assignable<decltype(std::declval<__type4>()(std::declval<__type22>()))>::type __type23;
      typedef decltype(std::declval<__type5>()(std::declval<__type11>(), std::declval<__type15>(), std::declval<__type18>())) __type27;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type16>())) __type29;
      typedef typename pythonic::assignable<decltype(std::declval<__type4>()(std::declval<__type27>(), std::declval<__type29>()))>::type __type30;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type31;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::round{})>::type>::type __type32;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::abs{})>::type>::type __type33;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type34;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type35;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type17>::type>::type __type36;
      typedef typename pythonic::lazy<__type36>::type __type37;
      typedef decltype(std::declval<__type35>()(std::declval<__type37>())) __type38;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type38>::type::iterator>::value_type>::type __type39;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type17>::type>::type __type40;
      typedef typename pythonic::lazy<__type40>::type __type41;
      typedef decltype(std::declval<__type35>()(std::declval<__type41>())) __type42;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type42>::type::iterator>::value_type>::type __type43;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type39>(), std::declval<__type43>())) __type44;
      typedef decltype(std::declval<__type34>()[std::declval<__type44>()]) __type45;
      typedef decltype(std::declval<__type33>()(std::declval<__type45>())) __type46;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type>::type __type47;
      typedef decltype(pythonic::operator_::div(std::declval<__type46>(), std::declval<__type47>())) __type48;
      typedef decltype(std::declval<__type32>()(std::declval<__type48>())) __type49;
      typedef decltype(std::declval<__type31>()(std::declval<__type49>())) __type50;
      typedef typename pythonic::lazy<__type50>::type __type51;
      typedef decltype(pythonic::operator_::sub(std::declval<__type11>(), std::declval<__type19>())) __type53;
      typedef typename pythonic::lazy<__type53>::type __type54;
      typedef typename __combined<__type51,__type54>::type __type55;
      typedef decltype(pythonic::operator_::sub(std::declval<__type15>(), std::declval<__type19>())) __type57;
      typedef typename pythonic::lazy<__type57>::type __type58;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::enumerate{})>::type>::type __type59;
      typedef pythonic::types::contiguous_slice __type63;
      typedef decltype(std::declval<__type16>()(std::declval<__type39>(), std::declval<__type43>(), std::declval<__type63>())) __type64;
      typedef typename pythonic::lazy<__type64>::type __type65;
      typedef decltype(pythonic::operator_::mul(std::declval<__type19>(), std::declval<__type65>())) __type67;
      typedef typename pythonic::lazy<__type67>::type __type68;
      typedef typename __combined<__type65,__type68>::type __type69;
      typedef decltype(std::declval<__type59>()(std::declval<__type69>())) __type70;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type70>::type::iterator>::value_type>::type __type71;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type71>::type>::type __type72;
      typedef typename pythonic::lazy<__type72>::type __type73;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type55>(), std::declval<__type58>(), std::declval<__type73>())) __type74;
      typedef indexable<__type74> __type75;
      typedef typename __combined<__type30,__type75>::type __type76;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type78;
      typedef typename pythonic::assignable<decltype(std::declval<__type78>()[std::declval<__type44>()])>::type __type82;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type0>::type>::type>::type __type83;
      typedef decltype(pythonic::operator_::div(std::declval<__type82>(), std::declval<__type83>())) __type84;
      typedef typename pythonic::assignable<decltype(std::declval<__type31>()(std::declval<__type84>()))>::type __type85;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type55>(), std::declval<__type85>(), std::declval<__type73>())) __type91;
      typedef indexable<__type91> __type92;
      typedef typename __combined<__type76,__type92>::type __type93;
      typedef decltype(pythonic::operator_::add(std::declval<__type85>(), std::declval<__type19>())) __type96;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type55>(), std::declval<__type96>(), std::declval<__type73>())) __type98;
      typedef indexable<__type98> __type99;
      typedef typename __combined<__type93,__type99>::type __type100;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type71>::type>::type __type102;
      typedef typename pythonic::lazy<__type102>::type __type103;
      typedef container<typename std::remove_reference<__type103>::type> __type104;
      typedef decltype(std::declval<__type14>()[std::declval<__type85>()]) __type108;
      typedef decltype(pythonic::operator_::sub(std::declval<__type82>(), std::declval<__type108>())) __type109;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type109>(), std::declval<__type83>()))>::type __type111;
      typedef decltype(pythonic::operator_::sub(std::declval<__type19>(), std::declval<__type111>())) __type112;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type71>::type>::type>::type __type114;
      typedef decltype(pythonic::operator_::mul(std::declval<__type112>(), std::declval<__type114>())) __type115;
      typedef container<typename std::remove_reference<__type115>::type> __type116;
      typedef decltype(pythonic::operator_::mul(std::declval<__type111>(), std::declval<__type114>())) __type119;
      typedef container<typename std::remove_reference<__type119>::type> __type120;
      typedef typename __combined<__type100,__type75,__type104,__type104,__type92,__type116,__type116,__type99,__type120,__type120>::type __type121;
      typedef decltype(std::declval<__type121>()(std::declval<__type63>(), std::declval<__type63>(), std::declval<__type19>())) __type122;
      typedef container<typename std::remove_reference<__type122>::type> __type123;
      typedef pythonic::types::fast_contiguous_slice __type125;
      typedef decltype(std::declval<__type121>()(std::declval<__type63>(), std::declval<__type63>(), std::declval<__type125>())) __type126;
      typedef pythonic::types::slice __type128;
      typedef decltype(std::declval<__type121>()(std::declval<__type63>(), std::declval<__type63>(), std::declval<__type128>())) __type129;
      typedef decltype(pythonic::operator_::add(std::declval<__type126>(), std::declval<__type129>())) __type130;
      typedef container<typename std::remove_reference<__type130>::type> __type131;
      typedef typename __combined<__type23,__type123,__type131>::type __type132;
      typedef decltype(pythonic::operator_::mul(std::declval<__type47>(), std::declval<__type83>())) __type135;
      typedef __type1 __ptype0;
      typedef __type3 __ptype1;
      typedef typename pythonic::returnable<decltype(pythonic::operator_::div(std::declval<__type132>(), std::declval<__type135>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type operator()(argument_type0&& field_k0k1omega, argument_type1&& khs, argument_type2&& kzs, argument_type3&& KX, argument_type4&& KZ, argument_type5&& KH) const
    ;
  }  ;
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.4.8"));
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
  typename compute_spectrum_kzkhomega::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type compute_spectrum_kzkhomega::operator()(argument_type0&& field_k0k1omega, argument_type1&& khs, argument_type2&& kzs, argument_type3&& KX, argument_type4&& KZ, argument_type5&& KH) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type3;
    typedef std::integral_constant<long,1> __type4;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type3>::type>::type __type6;
    typedef indexable_container<__type4, typename std::remove_reference<__type6>::type> __type7;
    typedef typename __combined<__type3,__type7>::type __type8;
    typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type8>()))>::type __type9;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type10;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type10>::type>::type __type12;
    typedef indexable_container<__type4, typename std::remove_reference<__type12>::type> __type13;
    typedef typename __combined<__type10,__type13>::type __type14;
    typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type14>()))>::type __type15;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type16;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type16>())) __type17;
    typedef typename pythonic::assignable<typename std::tuple_element<2,typename std::remove_reference<__type17>::type>::type>::type __type18;
    typedef decltype(std::declval<__type1>()(std::declval<__type9>(), std::declval<__type15>(), std::declval<__type18>())) __type19;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, std::declval<__type16>())) __type21;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type19>(), std::declval<__type21>()))>::type __type22;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type23;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::round{})>::type>::type __type24;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::abs{})>::type>::type __type25;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type26;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type27;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type17>::type>::type __type28;
    typedef typename pythonic::lazy<__type28>::type __type29;
    typedef decltype(std::declval<__type27>()(std::declval<__type29>())) __type30;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type30>::type::iterator>::value_type>::type __type31;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type17>::type>::type __type32;
    typedef typename pythonic::lazy<__type32>::type __type33;
    typedef decltype(std::declval<__type27>()(std::declval<__type33>())) __type34;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type34>::type::iterator>::value_type>::type __type35;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type31>(), std::declval<__type35>())) __type36;
    typedef decltype(std::declval<__type26>()[std::declval<__type36>()]) __type37;
    typedef decltype(std::declval<__type25>()(std::declval<__type37>())) __type38;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type3>::type>::type>::type __type39;
    typedef decltype(pythonic::operator_::div(std::declval<__type38>(), std::declval<__type39>())) __type40;
    typedef decltype(std::declval<__type24>()(std::declval<__type40>())) __type41;
    typedef decltype(std::declval<__type23>()(std::declval<__type41>())) __type42;
    typedef typename pythonic::lazy<__type42>::type __type43;
    typedef long __type45;
    typedef decltype(pythonic::operator_::sub(std::declval<__type9>(), std::declval<__type45>())) __type46;
    typedef typename pythonic::lazy<__type46>::type __type47;
    typedef typename __combined<__type43,__type47>::type __type48;
    typedef decltype(pythonic::operator_::sub(std::declval<__type15>(), std::declval<__type45>())) __type50;
    typedef typename pythonic::lazy<__type50>::type __type51;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::enumerate{})>::type>::type __type52;
    typedef pythonic::types::contiguous_slice __type56;
    typedef decltype(std::declval<__type16>()(std::declval<__type31>(), std::declval<__type35>(), std::declval<__type56>())) __type57;
    typedef typename pythonic::lazy<__type57>::type __type58;
    typedef decltype(pythonic::operator_::mul(std::declval<__type45>(), std::declval<__type58>())) __type60;
    typedef typename pythonic::lazy<__type60>::type __type61;
    typedef typename __combined<__type58,__type61>::type __type62;
    typedef decltype(std::declval<__type52>()(std::declval<__type62>())) __type63;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type63>::type::iterator>::value_type>::type __type64;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type64>::type>::type __type65;
    typedef typename pythonic::lazy<__type65>::type __type66;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type48>(), std::declval<__type51>(), std::declval<__type66>())) __type67;
    typedef indexable<__type67> __type68;
    typedef typename __combined<__type22,__type68>::type __type69;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type71;
    typedef typename pythonic::assignable<decltype(std::declval<__type71>()[std::declval<__type36>()])>::type __type75;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type10>::type>::type>::type __type76;
    typedef decltype(pythonic::operator_::div(std::declval<__type75>(), std::declval<__type76>())) __type77;
    typedef typename pythonic::assignable<decltype(std::declval<__type23>()(std::declval<__type77>()))>::type __type78;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type48>(), std::declval<__type78>(), std::declval<__type66>())) __type84;
    typedef indexable<__type84> __type85;
    typedef typename __combined<__type69,__type85>::type __type86;
    typedef decltype(pythonic::operator_::add(std::declval<__type78>(), std::declval<__type45>())) __type89;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type48>(), std::declval<__type89>(), std::declval<__type66>())) __type91;
    typedef indexable<__type91> __type92;
    typedef typename __combined<__type86,__type92>::type __type93;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type64>::type>::type __type95;
    typedef typename pythonic::lazy<__type95>::type __type96;
    typedef container<typename std::remove_reference<__type96>::type> __type97;
    typedef decltype(std::declval<__type14>()[std::declval<__type78>()]) __type101;
    typedef decltype(pythonic::operator_::sub(std::declval<__type75>(), std::declval<__type101>())) __type102;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type102>(), std::declval<__type76>()))>::type __type104;
    typedef decltype(pythonic::operator_::sub(std::declval<__type45>(), std::declval<__type104>())) __type105;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type64>::type>::type>::type __type107;
    typedef decltype(pythonic::operator_::mul(std::declval<__type105>(), std::declval<__type107>())) __type108;
    typedef container<typename std::remove_reference<__type108>::type> __type109;
    typedef decltype(pythonic::operator_::mul(std::declval<__type104>(), std::declval<__type107>())) __type112;
    typedef container<typename std::remove_reference<__type112>::type> __type113;
    typedef decltype(pythonic::operator_::add(std::declval<__type18>(), std::declval<__type45>())) __type119;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::functor::floordiv()(std::declval<__type119>(), std::declval<__type45>()))>::type __type120;
    typedef decltype(std::declval<__type1>()(std::declval<__type9>(), std::declval<__type15>(), std::declval<__type120>())) __type121;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type121>()))>::type __type122;
    typedef typename __combined<__type93,__type68,__type97,__type85,__type109,__type92,__type113>::type __type123;
    typedef decltype(std::declval<__type123>()(std::declval<__type56>(), std::declval<__type56>(), std::declval<__type45>())) __type124;
    typedef container<typename std::remove_reference<__type124>::type> __type125;
    typedef pythonic::types::fast_contiguous_slice __type127;
    typedef decltype(std::declval<__type123>()(std::declval<__type56>(), std::declval<__type56>(), std::declval<__type127>())) __type128;
    typedef pythonic::types::slice __type130;
    typedef decltype(std::declval<__type123>()(std::declval<__type56>(), std::declval<__type56>(), std::declval<__type130>())) __type131;
    typedef decltype(pythonic::operator_::add(std::declval<__type128>(), std::declval<__type131>())) __type132;
    typedef container<typename std::remove_reference<__type132>::type> __type133;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type30>::type::iterator>::value_type>::type>::type ik0;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type34>::type::iterator>::value_type>::type>::type ik1;
    typename pythonic::assignable_noescape<decltype(std::get<1>(khs))>::type deltakh = std::get<1>(khs);
    typename pythonic::assignable_noescape<decltype(std::get<1>(kzs))>::type deltakz = std::get<1>(kzs);
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::len{}(khs))>::type nkh = pythonic::builtins::functor::len{}(khs);
    typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::len{}(kzs))>::type nkz = pythonic::builtins::functor::len{}(kzs);
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1omega)))>::type nk0 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1omega));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1omega)))>::type nk1 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1omega));
    typename pythonic::assignable_noescape<decltype(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1omega)))>::type nomega = std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, field_k0k1omega));
    typename pythonic::assignable<typename __combined<__type93,__type68,__type97,__type85,__type109,__type92,__type113>::type>::type spectrum_kzkhomega = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(nkz, nkh, nomega), pythonic::builtins::getattr(pythonic::types::attr::DTYPE{}, field_k0k1omega));
    {
      long  __target140412140502512 = nk0;
      for (long  ik0=0L; ik0 < __target140412140502512; ik0 += 1L)
      {
        {
          long  __target140412140538800 = nk1;
          for (long  ik1=0L; ik1 < __target140412140538800; ik1 += 1L)
          {
            typename pythonic::lazy<__type62>::type values = field_k0k1omega(ik0,ik1,pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None));
            if (pythonic::operator_::ne(KX.fast(pythonic::types::make_tuple(ik0, ik1)), 0.0))
            {
              values = pythonic::operator_::mul(2L, values);
            }
            typename pythonic::assignable_noescape<decltype(KH.fast(pythonic::types::make_tuple(ik0, ik1)))>::type kappa = KH.fast(pythonic::types::make_tuple(ik0, ik1));
            typename pythonic::assignable_noescape<decltype(pythonic::builtins::functor::int_{}(pythonic::operator_::div(kappa, deltakh)))>::type ikh = pythonic::builtins::functor::int_{}(pythonic::operator_::div(kappa, deltakh));
            typename pythonic::lazy<__type48>::type ikz = pythonic::builtins::functor::int_{}(pythonic::builtins::functor::round{}(pythonic::operator_::div(pythonic::builtins::functor::abs{}(KZ.fast(pythonic::types::make_tuple(ik0, ik1))), deltakz)));
            if (pythonic::operator_::ge(ikz, pythonic::operator_::sub(nkz, 1L)))
            {
              ikz = pythonic::operator_::sub(nkz, 1L);
            }
            if (pythonic::operator_::ge(ikh, pythonic::operator_::sub(nkh, 1L)))
            {
              typename pythonic::lazy<decltype(pythonic::operator_::sub(nkh, 1L))>::type ikh_ = pythonic::operator_::sub(nkh, 1L);
              {
                for (auto&& __tuple0: pythonic::builtins::functor::enumerate{}(values))
                {
                  typename pythonic::lazy<decltype(std::get<1>(__tuple0))>::type value = std::get<1>(__tuple0);
                  typename pythonic::lazy<decltype(std::get<0>(__tuple0))>::type i = std::get<0>(__tuple0);
                  spectrum_kzkhomega[pythonic::types::make_tuple(ikz, ikh_, i)] += value;
                }
              }
            }
            else
            {
              typename pythonic::assignable_noescape<decltype(pythonic::operator_::div(pythonic::operator_::sub(kappa, khs[ikh]), deltakh))>::type coef_share = pythonic::operator_::div(pythonic::operator_::sub(kappa, khs[ikh]), deltakh);
              {
                for (auto&& __tuple1: pythonic::builtins::functor::enumerate{}(values))
                {
                  typename pythonic::assignable_noescape<decltype(std::get<1>(__tuple1))>::type value_ = std::get<1>(__tuple1);
                  typename pythonic::lazy<decltype(std::get<0>(__tuple1))>::type i_ = std::get<0>(__tuple1);
                  spectrum_kzkhomega[pythonic::types::make_tuple(ikz, ikh, i_)] += pythonic::operator_::mul(pythonic::operator_::sub(1L, coef_share), value_);
                  spectrum_kzkhomega[pythonic::types::make_tuple(ikz, pythonic::operator_::add(ikh, 1L), i_)] += pythonic::operator_::mul(coef_share, value_);
                }
              }
            }
          }
        }
      }
    }
    typename pythonic::assignable_noescape<decltype(pythonic::operator_::functor::floordiv()(pythonic::operator_::add(nomega, 1L), 2L))>::type nomega_ = pythonic::operator_::functor::floordiv()(pythonic::operator_::add(nomega, 1L), 2L);
    typename pythonic::assignable<typename __combined<__type122,__type125,__type133>::type>::type spectrum_onesided = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(nkz, nkh, nomega_));
    spectrum_onesided(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),0L) = spectrum_kzkhomega(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),0L);
    spectrum_onesided(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(1L,pythonic::builtins::None)) = pythonic::operator_::add(spectrum_kzkhomega(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::fast_contiguous_slice(1L,nomega_)), spectrum_kzkhomega(pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::contiguous_slice(pythonic::builtins::None,pythonic::builtins::None),pythonic::types::slice(-1L,pythonic::operator_::neg(nomega_),-1L)));
    return pythonic::operator_::div(spectrum_onesided, pythonic::operator_::mul(deltakz, deltakh));
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_spatiotemporal_spectra::__transonic__()());
typename __pythran_spatiotemporal_spectra::compute_spectrum_kzkhomega::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type compute_spectrum_kzkhomega0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& field_k0k1omega, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& khs, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& kzs, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& KX, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& KZ, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& KH) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_spatiotemporal_spectra::compute_spectrum_kzkhomega()(field_k0k1omega, khs, kzs, KX, KZ, KH);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_spatiotemporal_spectra::compute_spectrum_kzkhomega::type<pythonic::types::ndarray<float,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>::result_type compute_spectrum_kzkhomega1(pythonic::types::ndarray<float,pythonic::types::pshape<long,long,long>>&& field_k0k1omega, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& khs, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& kzs, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& KX, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& KZ, pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>&& KH) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_spatiotemporal_spectra::compute_spectrum_kzkhomega()(field_k0k1omega, khs, kzs, KX, KZ, KH);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_compute_spectrum_kzkhomega0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"field_k0k1omega", "khs", "kzs", "KX", "KZ", "KH",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[5]))
        return to_python(compute_spectrum_kzkhomega0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_spectrum_kzkhomega1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"field_k0k1omega", "khs", "kzs", "KX", "KZ", "KH",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<float,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[5]))
        return to_python(compute_spectrum_kzkhomega1(from_python<pythonic::types::ndarray<float,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_spectrum_kzkhomega(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_spectrum_kzkhomega0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_spectrum_kzkhomega1(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_spectrum_kzkhomega", "\n""    - compute_spectrum_kzkhomega(float64[:,:,:], float64[:], float64[:], float64[:,:], float64[:,:], float64[:,:])\n""    - compute_spectrum_kzkhomega(float32[:,:,:], float64[:], float64[:], float64[:,:], float64[:,:], float64[:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_spectrum_kzkhomega",
    (PyCFunction)__pythran_wrapall_compute_spectrum_kzkhomega,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the kz-kh-omega spectrum.\n""\n""    Supported prototypes:\n""\n""    - compute_spectrum_kzkhomega(float64[:,:,:], float64[:], float64[:], float64[:,:], float64[:,:], float64[:,:])\n""    - compute_spectrum_kzkhomega(float32[:,:,:], float64[:], float64[:], float64[:,:], float64[:,:], float64[:,:])"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "spatiotemporal_spectra",            /* m_name */
    "",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(spatiotemporal_spectra)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(spatiotemporal_spectra)(void) {
    import_array()
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("spatiotemporal_spectra",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.9.11",
                                      "2021-06-01 17:17:25.692132",
                                      "677958e77175934914d79304cf8e3dedbde70078c3bc1722b394ba1d29fca00f");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);

    PyModule_AddObject(theModule, "__transonic__", __transonic__);
    PYTHRAN_RETURN;
}

#endif